from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import AccessKey


class RegisterValidSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise ValidationError('username already exist')
        except User.DoesNotExist:
            return username

    def validate_password(self, password):
        if password.__len__() < 4:
            raise ValidationError('password too short')
        return password


class LoginValidSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    user = None

    def validate_username(self, username):
        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('username does not exist')

        return username

    def validate_password(self, password):
        if self.user:
            if not self.user.check_password(password):
                raise ValidationError('password error')
        return password


class AccessKeyValidSerializer(serializers.Serializer):
    access_key = serializers.CharField()
    user = None

    def validate_access_key(self, access_key):
        try:
            key = AccessKey.objects.get(key=access_key)
            if (timezone.now() - key.create_time).total_seconds() > 300:
                key.delete()
                raise ValidationError('Timeout access key')
            self.user = User.objects.get(username=key.user)
        except AccessKey.DoesNotExist:
            raise ValidationError('Error access key')
        return access_key

