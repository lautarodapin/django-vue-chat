from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Chat, Message
from users.serializers import UserSerializer
from users.models import User


class ChatSerializer(serializers.ModelSerializer):
    users = PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    active_users = UserSerializer(read_only=True, many=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'name',
            'created_at',
            'mod_at',
            'created_by',
            'mod_by',
            'users',
            'active_users',
            'last_message',
            'unread_count',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user

    def get_last_message(self, obj: Chat):
        return MessageSerializer(obj.messages.first()).data

    def get_unread_count(self, obj: Chat) -> int:
        return (
            obj.messages.filter(read=False)
            .exclude(created_by=self.user)
            .count()
        )


class MinimalChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'name',
            'created_at',
            'mod_at',
        ]

class MessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True, many=False)
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'chat',
            'created_by',
            'created_at',
            'mod_at',
            'read',
        ]
