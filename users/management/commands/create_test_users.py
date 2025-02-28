from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания тестовых пользователей"""

    def handle(self, *args, **options):

        User = get_user_model()

        try:
            group = Group.objects.get(name="Менеджер")
        except ObjectDoesNotExist:
            group = Group.objects.create(name="Менеджер")
            cancel_mailing_permission = Permission.objects.get(
                codename="can_cancel_mailing"
            )
            block_user_permission = Permission.objects.get(codename="can_block_user")
            group.permissions.add(cancel_mailing_permission, block_user_permission)
            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно создана группа {group.name} c правами "{cancel_mailing_permission}" и "{block_user_permission}"'
                )
            )

        # создание менеджера
        try:
            user = User.objects.get(email="manager@manager.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="manager@manager.ru",
        )
        user.set_password("123qwe456rty")
        user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан модератор с email {user.email} с паролем 123qwe456rty и добавлен в группу {group.name}"
            )
        )

        # создание тестового юзера №1
        try:
            user = User.objects.get(email="test1@test1.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="test1@test1.ru",
        )
        user.set_password("123qwe456rty")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )

        # создание тестового юзера №2
        try:
            user = User.objects.get(email="test2@test2.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="test2@test2.ru",
        )
        user.set_password("123qwe456rty")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )
