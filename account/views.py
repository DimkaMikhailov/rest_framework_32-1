import binascii, os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from account.serializers import LoginValidSerializer, RegisterValidSerializer, AccessKeyValidSerializer
from account.models import AccessKey
from datetime import timedelta


@api_view(['POST'])
def register_api_view(request):
    serializer = RegisterValidSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_201_CREATED, data={'message': 'user create successfully', 'user': user.id})


@api_view(['POST'])
def login_api_view(request):
    serializer = LoginValidSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    login_user = serializer.user
    if login_user.is_active:
        token, _ = Token.objects.get_or_create(user=login_user)
        return Response(status=status.HTTP_200_OK, data={
            'message': 'login successfully',
            'user': login_user.pk,
            'key': token.key
        })
    else:
        key = binascii.hexlify(os.urandom(3)).decode()
        AccessKey.objects.create(key=key, user=login_user)
        # Send key to e-mail user
        return Response(data={'message': 'confirm account'}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def confirm_api_view(request):
    serializer = AccessKeyValidSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    AccessKey.objects.filter(user=serializer.user).delete()
    user = serializer.user
    user.is_active = True
    user.save()
    return Response(data={
        'message': 'confirm successfully',
        'user_id': serializer.user.id,
    })
