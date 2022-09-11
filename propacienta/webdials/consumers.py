# import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class WebDialsSignalConsumer(JsonWebsocketConsumer):
    online_users = dict()
    channel_layer = "webdials"

    def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            # отключает неавторизованных пользователей
            self.close(close_code=1008)
        self.add_online_user(user, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(str(user.id), self.channel_name)
        self.send_user_connect(user)
        self.accept()

    def disconnect(self, close_code):
        user = self.scope['user']
        self.delete_online_user(user, self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(str(user.id), self.channel_name)

    def receive_json(self, content):
        self.return_type_receiver_handler(content)

    def send_json(self, content, close=False):
        content = content["content"]
        return super().send_json(content, close)

    def add_online_user(self, user, channel):
        """
        Добавляем канал в группу пользователя для доставки сообщений
        во все активные каналы (открытые клиенты) пользователя
        """
        if user.id not in self.online_users:
            self.online_users[user.id] = list()
        self.online_users[user.id].append(channel)

    def delete_online_user(self, user, channel):
        """
        Удаление канала из группы пользователя.
        Если открытых каналов не осталось, разослать другим пользователям сообщение
        об отключении текущего.
        """
        if user.id in self.online_users:
            self.online_users[user.id] = list(
                filter(lambda x: x != channel, self.online_users[user.id])
            )
        if len(self.online_users[user.id]) == 0:
            self.send_user_disconnect(user)

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
