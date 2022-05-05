import datetime as dt

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CredentialsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'password': {'required': False}}

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email

    def validate_username(self, value):
        username_me = value.lower()
        if 'me' == username_me:
            raise serializers.ValidationError(
                f'Создание Пользователя c username "{username_me}" запрещено'
            )
        return value


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        ]
        read_only_fields = ['role']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        ]

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(*args, **kwargs)
        # Определяем новое поле
        self.fields['confirmation_code'] = serializers.CharField(required=True)

        # Удаляем поля по умолчанию от аутентификации django
        del self.fields['password']

    def validate(self, attrs):
        """Переопределяем валидатор под требуемые условия наших входных данных.
        """
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        # Условия если пользователя нет и код не корректен
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise ValidationError(detail='Код валидации не корректен')

        # Структра отправки для токена
        data = {}
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class PostTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if dt.date.today().year < value and value > 0:
            raise serializers.ValidationError(
                'Неправильно указан год'
            )
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id'),
            author = self.context['request'].user
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на этот обзор.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
