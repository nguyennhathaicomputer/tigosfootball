from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    pass

    def __str__(self):
        return self.username