import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdministratorRole
from .serializers import (
    CredentialsSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserRoleSerializer,
)

User = get_user_model()


class SignUpViewSet(viewsets.ModelViewSet):
    """Обработка принимает на вход параметры POST запросом:
    email и username, генерирует verification_code,
    создает пользователя и отправляет
    код по указаноий в параметре почте.
    Данный узел свободен от аутентификации и разрешений.
    """
    queryset = User.objects.all()
    serializer_class = CredentialsSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request):
        serializer = CredentialsSerializer(data=request.data)
        if serializer.is_valid():
            # Код подтверждения
            confirmation_code = random.randrange(1111, 9999)
            serializer.save(confirmation_code=confirmation_code)

            # Отправка письма
            mail_text = f'Код подтверждения {confirmation_code}'
            mail_theme = 'Код подтверждения'
            mail_from = 'from@example.com'
            mail_to = serializer.data['email']

            send_mail(mail_theme,
                      mail_text,
                      mail_from,
                      [mail_to],
                      fail_silently=False,
                      )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    "Обработка выдачи токенов."
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Операции связананные с Users"""
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdministratorRole,)

    @action(detail=False, methods=['PATCH', 'GET'],
            url_path='me',
            permission_classes=[IsAuthenticated],)
    def me_user(self, request, pk=None):
        """Обработка узла users/me"""
        user = User.objects.get(username=request.user)
        serializer = UserRoleSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
