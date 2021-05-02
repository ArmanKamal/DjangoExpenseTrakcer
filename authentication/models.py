from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(models.Manager):
    def regsiter_validation_view(self,postData):
        errors = {}
        if  User.objects.filter(username=postData['username']).exists():
            errors['messages'] = "Username already exists"
        return errors
            



class User(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    objects = UserManager()

