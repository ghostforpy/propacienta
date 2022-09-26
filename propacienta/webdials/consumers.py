from time import sleep
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.db.models import F
from django.utils import timezone

from .coturn import get_coturn_credentials
from .models import WebDial

default_cache = caches['default']

User = get_user_model()


class Dial:
    INIT_STATE = "init"
    ACCEPT_STATE = "accept"
    IN_CALL_STATE = "in_call"

    def __init__(
            self,
            uuid,
            initiator,
            opponent,
            initiator_channel,
            opponent_channel,
            state=INIT_STATE
                ) -> None:
        self.uuid = uuid
        self.initiator = initiator
        self.initiator_channel = initiator_channel
        self.opponent = opponent
        self.opponent_channel = opponent_channel
        self.state = state
        self.webdial = None


class WebDialsSignalConsumer(JsonWebsocketConsumer):
    default_cache = default_cache
    user_cache_format = "user_{}"
    default_max_age = 3600  # 1 час
    online_users = dict()
    doctors_ids = dict()
    pacients_ids = dict()
    dials = dict()
    channel_layer = "webdials"

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
        content = {"event": "get_coturn_credentials"}
        content["credentials"] = credentials
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            self.channel_name, content,
        )

    def disconnect(self, close_code):
        user = self.scope['user']
        self.websocket_disconnect_end_call()
        self.delete_online_user(user)

    def send_json(self, content, close=False):
        del content["type"]
        return super().send_json(content, close)

    def add_online_user(self, user):
        """
        Для каждого пользователя должен быть открыт только один канал.
        """
        if user.doctor is not None:
            try:
                self.doctors_ids[user.doctor.id] = user.id
            except Exception as e:
                print(e)
        self.pacients_ids[user.pacient.id] = user.id
        if user.id in self.online_users:
            try:
                self.online_users[user.id].close()
            except Exception as e:
                print(e)
        self.online_users[user.id] = self

    def delete_online_user(self, user):
        """
        Удаление канала.
        """
        if user.id in self.online_users:
            if self.online_users[user.id] != self:
                return
            del self.online_users[user.id]
            if user.doctor is not None:
                try:
                    if user.doctor.id in self.doctors_ids:
                        del self.doctors_ids[user.doctor.id]
                except Exception as e:
                    print(e)
            if user.pacient.id in self.pacients_ids:
                del self.pacients_ids[user.pacient.id]

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
            opponent_channel.channel_name, content,
        )

    def return_opponent_user_id(self, content):
        dial_uuid = content["dial_uuid"]
        self_id = self.scope['user'].id
        dial = self.dials[dial_uuid]
        if dial["initiator"] == self_id:
            opponent_id = dial["opponent"]
        elif dial["opponent"] == self_id:
            opponent_id = dial["initiator"]
        return opponent_id

    def return_opponent_channel(self, content):
        opponent_id = self.return_opponent_user_id(content)
        return self.online_users[opponent_id]

    def add_user_to_cache(self, user):
        self.default_cache.add(self.user_cache_format.format(id), user, self.default_max_age)

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
            opponent_channel.channel_name, content,
        )

    def candidate_handler(self, content):
        sleep(0.5)
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )

    def user_is_on_call(self, user_id):
        for i in self.dials:
            if self.dials[i]["initiator"] == user_id or self.dials[i]["opponent"] == user_id:
                return True
        return False

    def return_reject_init_call(self, reason=None):
        """Вернуть инициатору вызова отбой без посылки вызова оппоненту."""
        content = dict()
        content["type"] = "send.json"
        content["event"] = "reject_init_call"
        content["reason"] = reason
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
                user_id = self.doctors_ids[opponent_id]
            elif opponent_type == "pacient":
                user_id = self.pacients_ids[opponent_id]
        except KeyError:
            # подумать может писать в базу
            return self.return_reject_init_call("opponent_is_offline")
        if user_id in self.online_users:
            if self.user_is_on_call(user_id):
                # подумать может писать в базу и отправлять уведомление
                return self.return_reject_init_call("opponent_is_busy")
            opponent_channel = self.online_users[user_id]
            dial_uuid = str(uuid4())
            self.dials[dial_uuid] = {"initiator": self_id, "opponent": user_id}
            content["type"] = "send.json"
            content["init_call_username"] = self.scope["user"].get_fio()
            content["dial_uuid"] = dial_uuid
            async_to_sync(self.channel_layer.send)(
                opponent_channel.channel_name, content,
            )
            self.add_user_to_cache(self.scope['user'])
        else:
            # opponent user is offline
            # подумать может писать в базу
            return self.return_reject_init_call("opponent_is_offline")

    def accept_init_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
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
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["reason"] = "opponent_reject"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
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
        content = dict()
        initiator = self.return_user_by_id(self.dials[dial_uuid]["initiator"])
        opponent = self.return_user_by_id(self.dials[dial_uuid]["opponent"])
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["event"] = "end_call"
        content["reason"] = "opponent_end_call"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )
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
        self_id = self.scope['user'].id
        dial_uuid = None
        for i in self.dials:
            if self.dials[i]["initiator"] == self_id or self.dials[i]["opponent"] == self_id:
                dial_uuid = i
                opponent_id = self.dials[i]["initiator"] \
                    if self.dials[i]["initiator"] != self_id \
                    else self.dials[i]["opponent"]
                opponent_channel = self.online_users[opponent_id]
                break
        if dial_uuid is None:
            return
        content = dict()
        initiator = self.return_user_by_id(self.dials[dial_uuid]["initiator"])
        opponent = self.return_user_by_id(self.dials[dial_uuid]["opponent"])
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["event"] = "end_call"
        content["reason"] = "websocket_disconnect_end_call"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )
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
        initiator = self.return_user_by_id(self.dials[dial_uuid]["initiator"])
        opponent = self.return_user_by_id(self.dials[dial_uuid]["opponent"])
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
        # try:
        return self.return_handler(content)
        # except Exception as e:
            # print(e)
