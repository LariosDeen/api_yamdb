from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CredentialsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,)

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'password': {'required': False},

        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(*args, **kwargs)
        # Определяем новое поле
        self.fields['confirmation_code'] = serializers.CharField(required=True)

        # Удаляем поля по умолчанию от аутентификации django
        del self.fields['password']

    def validate(self, attrs):
        """Переопределяем валидатор
        под требуемые условия наших входных данных."""
        username = attrs.get("username")
        confirmation_code = attrs.get("confirmation_code")

        # Условия если пользователя нет и код не корректен
        user = get_object_or_404(
            User, username=username)
        if user.confirmation_code != confirmation_code:
            raise ValidationError(
                detail="Код валидации не корректен"
            )

        # Структра отправки для токена
        data = {}
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
