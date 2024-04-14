from django.core.management import BaseCommand

from config.settings import TELEGRAM_TEST_USERNAME
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='adelinazima@mail.ru',
            first_name='Adelina',
            last_name='Zimina',
            is_staff=True,
            is_superuser=True,
            telegram_username=TELEGRAM_TEST_USERNAME
        )
        user.set_password('1310')
        user.save()
