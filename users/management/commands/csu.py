from typing import Any

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """ creating a superuser """
        user = User.objects.create(
            email='kass.o@yandex.ru',
            first_name='mary',
            last_name='mary',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('12345')
        user.save()
