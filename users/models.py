from django.db.models import ImageField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    img = ImageField(upload_to='users_images', null=True, blank=True)
