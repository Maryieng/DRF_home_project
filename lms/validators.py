import re
from rest_framework.serializers import ValidationError


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """ Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com """
        reg = re.compile('^https://www.youtube.com/')
        field_value = dict(value).get(self.field)
        if not bool(reg.match(field_value)):
            raise 400
