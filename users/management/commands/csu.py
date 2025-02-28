from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания суперпользователя"""

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            User.objects.get(phone="111").delete()
        except ObjectDoesNotExist:
            pass
        user = User.objects.create(
            phone="111",
        )
        user.set_password("123qwe456rty")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Успешно создан суперпользователь с телефоном {user.phone}")
        )
