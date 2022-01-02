from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer


class UserConsumer(
    ListModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]