# import json

from time import sleep
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .coturn import get_coturn_credentials


class WebDialsSignalConsumer(JsonWebsocketConsumer):
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

    def return_opponent_channel(self, content):
        dial_uuid = content["dial_uuid"]
        self_id = self.scope['user'].id
        dial = self.dials[dial_uuid]
        if dial["initiator"] == self_id:
            opponent_id = dial["opponent"]
        elif dial["opponent"] == self_id:
            opponent_id = dial["initiator"]
        return self.online_users[opponent_id]

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
            return self.return_reject_init_call("opponent_is_offline")
        if user_id in self.online_users:
            if self.user_is_on_call(user_id):
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
        else:
            # user is offline
            return self.return_reject_init_call("opponent_is_offline")

    def accept_init_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        content["type"] = "send.json"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )

    def reject_init_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        dial_uuid = content["dial_uuid"]
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["reason"] = "opponent_reject"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )

    def handle_end_call(self, content):
        opponent_channel = self.return_opponent_channel(content)
        dial_uuid = content["dial_uuid"]
        content = dict()
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["event"] = "end_call"
        content["reason"] = "opponent_end_call"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
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
        del self.dials[dial_uuid]
        content["type"] = "send.json"
        content["event"] = "end_call"
        content["reason"] = "websocket_disconnect_end_call"
        async_to_sync(self.channel_layer.send)(
            opponent_channel.channel_name, content,
        )

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
        else:
            print(content)

    def receive_json(self, content):
        try:
            return self.return_handler(content)
        except Exception as e:
            print(e)
