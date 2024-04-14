from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('Введите email: ')
        telegram_username = input('Введите ник в телеграме: ')
        password = input('Введите пароль: ')
        user = User.objects.create(
            email=email,
            is_staff=False,
            is_superuser=False,
            telegram_username=telegram_username
        )
        user.set_password(password)
        user.save()
