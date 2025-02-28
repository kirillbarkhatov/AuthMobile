from django.contrib.auth.models import AbstractUser
from django.db import models
from users.services import generate_invite_code
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.core.cache import cache


class User(AbstractUser):
    """Модель кастомного пользователя"""

    username = None
    phone = PhoneNumberField(region="RU", unique=True, verbose_name="Телефон")
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code, verbose_name="Инвайт-код")
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="invited_users", verbose_name="Инвайт-код пригласившего пользователя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первой авторизации")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def generate_code(self):
        code = str(random.randint(1000, 9999))  # Генерация 4-значного кода
        cache.set(f"user_{self.phone}_code", code, timeout=300)  # Сохраняем код в кэше на 5 минут
        return code

    def check_code(self, code):
        cached_code = cache.get(f"user_{self.phone}_code")
        return cached_code == code

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
