from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def validate(self, attrs):
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)

        if password1 != password2:
            raise serializers.ValidationError('Las contraseñas deben coincidir')
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data, password=password)


class UserSerializer(serializers.ModelSerializer):
    auth_token = TokenSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'auth_token',
        ]

