import logging
import threading
from time import sleep
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.db.models import F
from django.utils import timezone

from .coturn import get_coturn_credentials
from .models import WebDial

default_cache = caches['default']

User = get_user_model()
# logger = logging.getLogger(__name__)
logger = logging.getLogger("sentry_sdk")


class WebDialsSignalConsumer(JsonWebsocketConsumer):
    default_cache = default_cache

    online_users_prefix = "webdials_online_user_{}"
    online_pacients_prefix = "webdials_online_pacient_{}"
    online_doctors_prefix = "webdials_online_doctor_{}"
    default_max_age_online_user = 86400  # 1 сутки
    active_dials_prefix = "webdials_active_dials_{}"

    user_cache_format = "user_{}"
    default_max_age = 3600  # 1 час

    channel_layer = "webdials"

    CONNECTING_TIOMEOUT = 10  # sec

    def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            # отключает неавторизованных пользователей
            self.close(close_code=1008)
        self.add_online_user(user)
        self.accept()
        self.send_coturn_credentials()

    def send_coturn_credentials(self):
        credentials = get_coturn_credentials(user_id=str(self.scope["user"].id))
        content = {
            "event": "get_coturn_credentials",
            "credentials": credentials,
            "type": "send.json"
            }
        async_to_sync(self.channel_layer.send)(self.channel_name, content,)

    def disconnect(self, close_code):
        user = self.scope['user']
        self.websocket_disconnect_end_call()
        self.delete_online_user(user)

    def send_json(self, content, close=False):
        del content["type"]
        return super().send_json(content, close)

    def set_online_doctor(self, doctor_id, user_id):
        self.default_cache.set(
            self.online_doctors_prefix.format(doctor_id),
            user_id,
            self.default_max_age_online_user
        )

    def set_online_pacient(self, pacient_id, user_id):
        self.default_cache.set(
            self.online_pacients_prefix.format(pacient_id),
            user_id,
            self.default_max_age_online_user
        )

    def add_online_user(self, user):
        """
        Для каждого пользователя должен быть открыт только один канал.
        """
        doctor_id = None
        if user.doctor is not None:
            try:
                doctor_id = user.doctor.id
                self.set_online_doctor(doctor_id, user.id)
            except Exception as e:
                logger.error(e)
        try:
            self.set_online_pacient(user.pacient.id, user.id)
        except Exception as e:
            logger.error(e)
        u = self.get_online_user(user.id)
        if u is not None:
            try:
                async_to_sync(self.channel_layer.send)(
                    u["channel"], {"type": "websocket.closebyname"},
                )
            except Exception as e:
                logger.error(e)
            u["channel"] = self.channel_name
        else:
            u = dict(
                user=user,
                channel=self.channel_name,
                doctor_id=doctor_id,
                pacient_id=user.pacient.id,
                status="online",
                dial_uuid=None
            )
        self.default_cache.set(
            self.online_users_prefix.format(user.id), u, self.default_max_age_online_user
        )

    def websocket_closebyname(self):
        self.close()

    def delete_online_user(self, user):
        """
        Удаление канала.
        """
        u = self.get_online_user(user.id)

        if u is not None:
            if u["channel"] != self.channel_name:
                #  if self.online_users[user.id] != self:
                return
            self.default_cache.delete(self.online_users_prefix.format(user.id))
            # del self.online_users[user.id]
            if user.doctor is not None:
                try:
                    self.default_cache.delete(self.online_doctors_prefix.format(user.doctor.id))
                    #  if user.doctor.id in self.doctors_ids:
                    #  del self.doctors_ids[user.doctor.id]
                except Exception as e:
                    print(e)
            self.default_cache.delete(self.online_pacients_prefix.format(user.pacient.id))
            # if user.pacient.id in self.pacients_ids:
            #     del self.pacients_ids[user.pacient.id]

    def get_online_user(self, user_id):
        return self.default_cache.get(self.online_users_prefix.format(user_id))

    def set_user_status(self, user_id, status, dial_uuid=None):
        user = self.get_online_user(user_id)
        if user is None:
            return
        user["status"] = status
        if status == 'in_dial':
            user["dial_uuid"] = dial_uuid
        else:
            user["dial_uuid"] = None
        self.default_cache.set(
            self.online_users_prefix.format(user_id),
            user,
            self.default_max_age_online_user
        )
        return user

    def get_dial(self, dial_uuid):
        return self.default_cache.get(self.active_dials_prefix.format(dial_uuid))

    def set_dial(self, dial_uuid, dial):
        self.default_cache.set(
            self.active_dials_prefix.format(dial_uuid),
            dial,
            self.default_max_age_online_user
        )

    def set_dial_state(self, dial_uuid, state):
        dial = self.get_dial(dial_uuid)
        if dial is not None:
            dial["state"] = state
            self.set_dial(dial_uuid, dial)
        return dial

    def delete_dial(self, dial_uuid):
        self.default_cache.delete(
            self.active_dials_prefix.format(dial_uuid),
        )

    def send_user_connect(self, user):
        """
        Разослать сообщение пользователям о подключении текущего пользователя.
        """
        # выбрать активных пользователей, с которыми у текущего пользователя есть чаты
        # разослать сообщение о подключении
        pass

    def send_user_disconnect(self, user):
        """
        Разослать сообщение пользователям об отключении текущего пользователя.
        """
        # выбрать активных пользователей, с которыми у текущего пользователя есть чаты
        # разослать сообщение об отключении
        pass

    def send_msg(self, user_id, content):
        async_to_sync(self.channel_layer.group_send)(
            str(user_id),
            {
                "type": "send.json",
                "content": content,
            },
        )

    def offer_handler(self, content):
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel, content,
        )

    def return_opponent_user_id(self, content):
        dial_uuid = content["dial_uuid"]
        self_id = self.scope['user'].id
        dial = self.get_dial(dial_uuid)
        if dial["initiator"] == self_id:
            opponent_id = dial["opponent"]
        elif dial["opponent"] == self_id:
            opponent_id = dial["initiator"]
        return opponent_id

    def return_opponent_channel(self, content):
        opponent_id = self.return_opponent_user_id(content)
        u = self.get_online_user(opponent_id)
        return u["channel"]

    def add_user_to_cache(self, user):
        self.default_cache.set(self.user_cache_format.format(id), user, self.default_max_age)

    def return_user_by_id(self, id):
        if self.default_cache.get(self.user_cache_format.format(id)) is not None:
            user = self.default_cache.get(self.user_cache_format.format(id))
        else:
            user = User.objects.get(id=id)
            self.add_user_to_cache(user)
        return user

    def answer_handler(self, content):
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel, content,
        )

    def candidate_handler(self, content):
        sleep(0.5)
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel, content,
        )

    def user_is_on_call(self, user_id):
        u = self.get_online_user(user_id)
        return u["status"] == "in_dial"

    def return_reject_init_call(self, reason=None):
        """Вернуть инициатору вызова отбой без посылки вызова оппоненту."""
        content = {
            "type": "send.json",
            "event": "reject_init_call",
            "reason": reason
        }
        async_to_sync(self.channel_layer.send)(
            self.channel_name, content,
        )

    def init_call(self, content):
        opponent_id = int(content["opponentId"])
        opponent_type = content["opponentType"]
        self_id = self.scope['user'].id
        if self.user_is_on_call(self_id):
            return self.return_reject_init_call("user_in_call")
        try:
            if opponent_type == "doctor":
                user_id = self.default_cache.get(self.online_doctors_prefix.format(opponent_id))
            elif opponent_type == "pacient":
                user_id = self.default_cache.get(self.online_pacients_prefix.format(opponent_id))
        except KeyError:
            # подумать может писать в базу
            return self.return_reject_init_call("opponent_is_offline")
        if user_id is None:
            return self.return_reject_init_call("opponent_is_offline")
        u = self.get_online_user(user_id)
        if u is not None:
            if self.user_is_on_call(user_id):
                # подумать может писать в базу и отправлять уведомление
                return self.return_reject_init_call("opponent_is_busy")
            opponent_channel = u["channel"]
            dial_uuid = str(uuid4())
            self.set_dial(dial_uuid, {"initiator": self_id, "opponent": user_id, "state": "init"})
            self.set_user_status(user_id, "in_dial", dial_uuid=dial_uuid)
            self.set_user_status(self_id, "in_dial", dial_uuid=dial_uuid)
            content["type"] = "send.json"
            content["init_call_username"] = self.scope["user"].get_fio()
            content["dial_uuid"] = dial_uuid
            if opponent_type == "pacient":
                content["avatar"] = self.scope["user"].doctor.avatar.url
            async_to_sync(self.channel_layer.send)(
                opponent_channel, content,
            )
            self.add_user_to_cache(self.scope['user'])

            def check_dial():
                sleep(self.CONNECTING_TIOMEOUT)  # таймаут ожидания установки соединения
                dial = self.get_dial(dial_uuid)
                if dial is not None:
                    print("dial", dial, dial["state"])
                    if dial["state"] != "connected":
                        for channel in [self.channel_name, opponent_channel]:
                            async_to_sync(self.channel_layer.send)(
                                channel,
                                {
                                    "type": "send.json",
                                    "dial_uuid": dial_uuid,
                                    "event": "init_call_failed"
                                },
                            )
                        for i in ["initiator", "opponent"]:
                            user_id = dial[i]
                            self.set_user_status(user_id, "online")
                        self.delete_dial(dial_uuid)
            thread = threading.Thread(target=check_dial)
            thread.start()

        else:
            # opponent user is offline
            # подумать может писать в базу
            return self.return_reject_init_call("opponent_is_offline")

    def accept_init_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        self.set_dial_state(content["dial_uuid"], "connecting")
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel, content,
        )
        WebDial.objects.create(
            initiator=self.return_user_by_id(id=self.return_opponent_user_id(content)),
            opponent=self.scope["user"],
            uuid=content["dial_uuid"]
        )

    def reject_init_call(self, content):
        """Послать инициатору вызова отбой по причине отказа оппонента принять вызов."""
        opponent_channel = self.return_opponent_channel(content)
        dial_uuid = content["dial_uuid"]
        initiator = self.return_user_by_id(id=self.return_opponent_user_id(content))
        self.delete_dial(dial_uuid)
        self.set_user_status(initiator.id, "online")
        self.set_user_status(self.scope["user"].id, "online")
        content["type"] = "send.json"
        content["reason"] = "opponent_reject"
        async_to_sync(self.channel_layer.send)(
            opponent_channel, content,
        )
        WebDial.objects.create(
            initiator=initiator,
            opponent=self.scope["user"],
            uuid=dial_uuid,
            end_webdial_reason="opponent_reject"
        )

    def handle_end_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        dial_uuid = content["dial_uuid"]
        dial = self.get_dial(dial_uuid)
        initiator = self.return_user_by_id(dial["initiator"])
        opponent = self.return_user_by_id(dial["opponent"])
        self.delete_dial(dial_uuid)
        self.set_user_status(initiator.id, "online")
        self.set_user_status(opponent.id, "online")
        content = {
            "type": "send.json",
            "event": "end_call",
            "reason": "opponent_end_call"
        }
        async_to_sync(self.channel_layer.send)(opponent_channel, content,)
        end_webdial_reason = "initiator" if initiator == self.scope["user"] else "opponent"
        now = timezone.now()
        WebDial.objects.filter(
            uuid=dial_uuid,
            initiator=initiator,
            opponent=opponent
        ).update(
            end_webdial=now,
            webdial_duration=now-F("start_webdial"),
            end_webdial_reason=end_webdial_reason
        )

    def websocket_disconnect_end_call(self):
        # подумать
        self_id = self.scope['user'].id
        u = self.get_online_user(self_id)
        if u["status"] != "in_dial":
            return
        dial_uuid = u["dial_uuid"]
        dial = self.get_dial(dial_uuid)
        initiator = self.return_user_by_id(dial["initiator"])
        opponent = self.return_user_by_id(dial["opponent"])
        opponent_id = opponent.id if initiator.id == self_id else initiator.id
        # u = self.get_online_user(opponent_id)
        u = self.set_user_status(opponent_id, "online")
        opponent_channel = u["channel"]
        content = {
            "type": "send.json",
            "event": "end_call",
            "reason": "websocket_disconnect_end_call"
        }
        async_to_sync(self.channel_layer.send)(opponent_channel, content,)
        now = timezone.now()
        WebDial.objects.filter(
            uuid=dial_uuid,
            initiator=initiator,
            opponent=opponent
        ).update(
            end_webdial=now,
            webdial_duration=now-F("start_webdial"),
        )

    def handle_connected_call(self, content):
        dial_uuid = content["dial_uuid"]
        dial = self.set_dial_state(dial_uuid, "connected")
        initiator = self.return_user_by_id(dial["initiator"])
        opponent = self.return_user_by_id(dial["opponent"])
        WebDial.objects.filter(
            uuid=dial_uuid,
            initiator=initiator,
            opponent=opponent
        ).update(webdial_happen=True)

    def return_handler(self, content):
        if content["event"] == "init_call":
            return self.init_call(content)
        elif content["event"] == "accept_init_call":
            return self.accept_init_call(content)
        elif content["event"] == "reject_init_call":
            return self.reject_init_call(content)
        elif content["event"] == "offer":
            return self.offer_handler(content)
        elif content["event"] == "answer":
            return self.answer_handler(content)
        elif content["event"] == "candidate":
            return self.candidate_handler(content)
        elif content["event"] == "end_call":
            return self.handle_end_call(content)
        elif content["event"] == "connected_call":
            return self.handle_connected_call(content)
        else:
            print(content)

    def receive_json(self, content):
        if settings.DEBUG:
            return self.return_handler(content)
        else:
            try:
                return self.return_handler(content)
            except Exception as e:
                logger.error(e)
