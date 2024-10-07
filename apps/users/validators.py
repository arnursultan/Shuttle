from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if len(value) < 8 or len(value) > 32:
        raise ValidationError("The password must contain 8 to 32 characters.")
    if not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', value):
        raise ValidationError("The password can only contain numbers and letters of the English alphabet.")
