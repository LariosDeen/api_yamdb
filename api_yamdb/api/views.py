import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CredentialsSerializer

User = get_user_model()


class SignUp(APIView):
    """Обработка принимает на вход параметры POST запросом:
    email и username, генерирует verification_code,
    сохряняет код при условии, что такой пользователь найден и отправляет
    код по указаноий в параметре почте.
    Данный узел свободен от аутентификации и разрешений.
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = CredentialsSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            username = serializer.data['username']
            user = get_object_or_404(User, username=username, email=email)
            print(serializer.data['username'])
            confirmation_code = random.randrange(1111, 9999)

            user.confirmation_code = confirmation_code
            user.save()

            mail_text = f'Код подтверждения {confirmation_code}'
            mail_theme = 'Код подтверждения'
            mail_from = 'from@example.com'
            mail_to = email

            send_mail(mail_theme,
                      mail_text,
                      mail_from,
                      [mail_to],
                      fail_silently=False,
                      )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = serializers.CharField(required=True)

        # Удаляем поля по умолчанию от аутентификации django
        del self.fields['password']

    def validate(self, attrs):
        username = attrs.get("username")
        confirmation_code = attrs.get("confirmation_code")

        user = get_object_or_404(
            User, username=username, confirmation_code=confirmation_code)

        # Структра для токена
        data = {}
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
