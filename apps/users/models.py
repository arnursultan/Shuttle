from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+1\d{10}$',
        message="The telephone number must be in the format: '+1XXXXXXXXXX'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.username
