from rest_framework import serializers, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import MinimalChatSerializer, ChatSerializer, MessageSerializer

class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=True, url_path='join-chat', permission_classes=[IsAuthenticated])
    def join_chat(self, request, **kwargs):
        instance: Chat = self.get_object()
        instance.active_users.add(request.user)
        return Response(self.get_serializer(instance=instance).data, status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=True, url_path='leave-chat', permission_classes=[IsAuthenticated])
    def leave_chat(self, request, **kwargs):
        instance: Chat = self.get_object()
        instance.active_users.remove(request.user)
        return Response(self.get_serializer(instance=instance).data, status=status.HTTP_202_ACCEPTED)

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['chat']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)