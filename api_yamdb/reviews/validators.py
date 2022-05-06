from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    if dt.date.today().year < value:
        raise ValidationError(
            'Год создания не может быть больше текущего'
        )
    return value
