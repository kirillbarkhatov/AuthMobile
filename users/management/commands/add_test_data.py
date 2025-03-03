from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Добавление данных из фикстур"

    def handle(self, *args, **kwargs):

        # Удаляем существующие записи
        User.objects.all().delete()

        # создание фикстур - команды для терминала
        # python -Xutf8 manage.py dumpdata users.User --output user_fixture.json --indent 4

        # Добавляем данные из фикстур
        call_command("loaddata", "users_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Пользователи загружены из фикстур успешно"))
