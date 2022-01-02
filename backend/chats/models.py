from django.db import models

from core.models import TimestampedModel
from users.models import User

class Chat(TimestampedModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='chats', blank=True)
    active_users = models.ManyToManyField(User, related_name='active_chats', blank=True)

    def __str__(self):
        return f'Chat: {self.name if self.name else str(self.id)}'
    

class Message(TimestampedModel):
    text = models.CharField(max_length=1024)
    chat = models.ForeignKey(Chat, models.SET_NULL, null=True, blank=False, related_name='messages')

    def __str__(self):
        return f'{self.created_by}: {self.text}' if self.created_by else 'Usuario borrado'
