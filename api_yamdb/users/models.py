from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'User'),
    ('admin', 'Administrator'),
    ('moderator', 'Moderator'),
)


class User(AbstractUser):

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True, max_length=50)
    role = models.CharField('Роль', max_length=10,
                            choices=ROLES, default='user')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user_email'),
        ]

        ordering = ['id']
