"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .middlewares import TokenAuthMiddleware

from users.consumers import UserConsumer
from chats.consumers import ChatConsumer
from .consumers import DemultiplexerConsumer


application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                re_path(r'^ws/$', DemultiplexerConsumer.as_asgi()),
                re_path(r'^ws/users/$', UserConsumer.as_asgi()),
                re_path(r'^ws/chats/$', ChatConsumer.as_asgi()),
            ])
        )
    )
})