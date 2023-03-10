from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import User
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.fields import PasswordField


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True, write_only=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'password и password_repeat должны совпадать '})
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_onli_fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def create(self, validated_data: dict) -> User:
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )
        ):
            raise AuthenticationFailed
        return user


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True, write_only=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, value: str) -> str:
        if not self.instance.check_password(value):
            raise ValidationError('')
        return value

    def update(self, instance, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance
