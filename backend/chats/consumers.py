from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin, CreateModelMixin
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated
from .models import User, Chat, Message
from .serializers import UserSerializer, ChatSerializer, MessageSerializer

class ChatConsumer(
    ListModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(users=self.scope['user']).distinct()

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        print('message_activity', message)
        await self.send_json(message)

    @message_activity.serializer
    def chat_activity(self, instance: Message, action, **kwargs):
        return MessageSerializer(instance=instance).data

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        # this block of code is called very often *DO NOT make DB QUERIES HERE*
        yield f'-chat__{instance.chat.id}'

    @message_activity.groups_for_consumer
    def message_activity(self, id=None, **kwargs):
        if id is not None:
            yield f'-chat__{id}'

    @action()
    async def subscribe_to_chat(self, id, **kwargs):
        await self.message_activity.subscribe(id=id)

    @action()
    async def unsubscribe_to_chat(self, id, **kwargs):
        await self.message_activity.unsubscribe(id=id)
        

class MessageConsumer(
    CreateModelMixin,
    ListModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset, filters=None, **kwargs):
        return queryset.filter(**filters) if filters else queryset

    def perform_create(self, serializer, **kwargs):
        instance: Message = serializer.save(created_by=self.scope['user'])
        Message.objects.filter(chat=instance.chat).exclude(created_by=self.scope['user']).update(read=True)
