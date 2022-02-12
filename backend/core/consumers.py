from channelsmultiplexer.demultiplexer import AsyncJsonWebsocketDemultiplexer
from chats.consumers import ChatConsumer, MessageConsumer
from users.consumers import UserConsumer


class DemultiplexerConsumer(AsyncJsonWebsocketDemultiplexer):
    applications = {
        'chats': ChatConsumer.as_asgi(),
        'users': UserConsumer.as_asgi(),
        'messages': MessageConsumer.as_asgi(),
    }
