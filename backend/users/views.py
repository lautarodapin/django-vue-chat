from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, TokenSerializer, RegisterSerializer
from rest_framework import serializers, status

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def current(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, serializer_class=RegisterSerializer, permission_classes=[AllowAny])
    def register(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=AuthTokenSerializer, permission_classes=[AllowAny])
    def login(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, **UserSerializer(instance=user).data}, status=status.HTTP_200_OK)
