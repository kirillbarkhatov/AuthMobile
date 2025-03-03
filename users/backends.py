from django.contrib.auth.backends import BaseBackend

from .models import User


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, code=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            if user.check_code(code):  # Проверка кода (см. шаг 3)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
