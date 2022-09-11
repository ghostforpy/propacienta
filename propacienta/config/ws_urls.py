from django.urls import re_path

from chats.consumers import ChatConsumer
from webdials.consumers import WebDialsSignalConsumer

websocket_urlpatterns = [
    re_path(r'ws/chats/$', ChatConsumer.as_asgi()),
    re_path(r'ws/webdials/$', WebDialsSignalConsumer.as_asgi()),
]
