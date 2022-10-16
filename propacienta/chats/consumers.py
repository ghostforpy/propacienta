# import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer  # , WebsocketConsumer
from django.core.cache import caches

from .api.serializers import DialogMessageSerializer
# from django.contrib.auth.models import AnonymousUser
from .models import Dialog, DialogMessage

# from rest_framework import serializers




# class DialogMessageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DialogMessage
#         fields = "__all__"


class ChatConsumer(JsonWebsocketConsumer):
    online_users = dict()
    default_cache = caches['default']
    online_users_prefix = "chats_online_user_{}"
    default_max_age_online_user = 86400  # 1 сутки

    TYPE_RECEIVER_HANDLERS = {
            "message": "message_receiver_handler",
            "service": "service_receiver_handler",
            "message_and_file": "message_and_file_receiver_handler",
            "message_and_image": "message_and_image_receiver_handler",
    }
    SERVICE_HANDLERS = {
        "typing": "typing_service_handler",
        "message_received_and_read": "message_received_and_read_handler",
        "message_received": "message_received_service_handler",
        "messages_read": "messages_read_service_handler",
    }

    def return_type_receiver_handler(self, content):
        # print(content)
        try:
            content_type = content["type"]
            handler = getattr(self, self.TYPE_RECEIVER_HANDLERS[content_type], None)
            if handler:
                handler(content)
            else:
                raise KeyError
        except KeyError:
            # вызывается в случае, если нет ключа "type" в content, а также в случае,
            # если ключ "type" неправильный или отсутсвует в списке разрешенных
            # отключает пользователей с неправильными форматами сообщений
            self.close(close_code=1007)

    def return_service_handler(self, content):
        try:
            service_type = content["message"]["service_type"]
            handler = getattr(self, self.SERVICE_HANDLERS[service_type], None)
            if handler:
                handler(content)
            else:
                raise KeyError
        except KeyError:
            # вызывается в случае, если нет ключа "type" в content, а также в случае,
            # если ключ "type" неправильный или отсутсвует в списке разрешенных
            # отключает пользователей с неправильными форматами сообщений
            self.close(close_code=1007)

    def service_receiver_handler(self, content):
        """
        content : {
            "type": "service",
            "message": {
                "service_type":
                    "message_received_and_read" | "message_received" | "messages_read" | "typing",
                "message_id": `message id`,
                "dialog": `dialog id`,
                "sender" : `sender user id`
            }
        }
        """
        print("service handler", content)
        self.return_service_handler(content)

    def typing_service_handler(self, content):
        pass

    def service_message_notifier(self, content):
        # print("service_message_notifier")
        dialog_id = int(content["message"]["dialog"])
        # dialog = Dialog.objects.prefetch_related("members").get(pk=dialog_id)
        sender_id = int(content["message"]["sender"])
        # to_user = dialog.members.exclude(id=sender_id).get()

        if content["message"]["service_type"] == "messages_read":
            self.send_msg(
                sender_id,
                {
                    "type": "service",
                    "service_type": content["message"]["service_type"],
                    "dialog": dialog_id,
                    "messages_ids": content["message"]["messages_ids"]
                }
            )
        else:
            self.send_msg(
                sender_id,
                {
                    "type": "service",
                    "service_type": content["message"]["service_type"],
                    "dialog": dialog_id,
                    "message_id": int(content["message"]["message_id"])
                }
            )

    def message_received_service_handler(self, content):
        message_id = int(content["message"]["message_id"])
        DialogMessage.objects.filter(pk=message_id).update(received_by_the_user=True)
        self.service_message_notifier(content)

    def messages_read_service_handler(self, content):
        messages_ids = [int(i) for i in content["message"]["messages_ids"]]
        DialogMessage.objects.filter(pk__in=messages_ids).update(read_by_the_user=True)
        self.service_message_notifier(content)

    def message_received_and_read_handler(self, content):
        # print("message_received_and_read_handler")
        message_id = int(content["message"]["message_id"])
        DialogMessage.objects.filter(pk=message_id).update(
            received_by_the_user=True, read_by_the_user=True
        )
        self.service_message_notifier(content)

    def message_and_file_receiver_handler(self, content):
        pass

    def message_and_image_receiver_handler(self, content):
        pass

    def message_receiver_handler(self, content):
        """
        content : {
            "type": "message",
            "to_user": `user id`,
            "message": {
                "sender": `sender user id`,
                "message": `message text`,
                "dialog": `chat id`
            }
        }
        """
        user = self.scope['user']
        message = content["message"]
        to_user = content["to_user"]
        # msg = DialogMessage.objects.create(**message)
        serializer = DialogMessageSerializer(data=message)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        content = {"type": "message", "message": serializer.data}
        self.send_msg(user.id, content)  # отправить подтверждение отправителю
        # self.send_msg(to_user, serializer.data)  # отправка сообщения по каналам
        self.send_msg(to_user, content)  # отправка сообщения по каналам

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
        user_channels = self.default_cache.get(self.online_users_prefix.format(user.id))
        if user_channels is None:
            user_channels = set()
        user_channels.add(channel)
        self.default_cache.set(
            self.online_users_prefix.format(user.id),
            user_channels,
            self.default_max_age_online_user
        )
        # if user.id not in self.online_users:
        #     self.online_users[user.id] = list()
        # self.online_users[user.id].append(channel)

    def delete_online_user(self, user, channel):
        """
        Удаление канала из группы пользователя.
        Если открытых каналов не осталось, разослать другим пользователям сообщение
        об отключении текущего.
        """
        user_channels = self.default_cache.get(self.online_users_prefix.format(user.id))
        if user_channels is set:
            user_channels.discard(channel)
            if len(user_channels) == 0:
                self.send_user_disconnect(user)
        # if user.id in self.online_users:
        #     self.online_users[user.id] = list(
        #         filter(lambda x: x != channel, self.online_users[user.id])
        #     )
        # if len(self.online_users[user.id]) == 0:
        #     self.send_user_disconnect(user)

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
