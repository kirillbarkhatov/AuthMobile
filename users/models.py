from django.contrib.auth.models import AbstractUser
from django.db import models
from users.servicies import generate_invite_code


class User(AbstractUser):
    """Моель кастомного пользователя"""

    username = None
    phone = models.CharField(
        max_length=15, unique=True, verbose_name="Телефон"
    )
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code, verbose_name="Инвайт-код")
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="invited_users", verbose_name="Инвайт-код пригласившего пользователя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первой авторизации")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
