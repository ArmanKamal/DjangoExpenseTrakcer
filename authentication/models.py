from django.db import models
import re
from django.contrib.auth.models import AbstractUser
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def regsiter_validation(self,postData):
        errors = {}
        if len(postData['username']) < 0:
            errors['password'] = "Useranme cannot be empty"
            if not str(postData['username']).isalnum():
                errors['username_al'] = "Username should contain only alphanumeric characters"
                if  User.objects.filter(username=postData['username']).exists():
                    errors['username'] = "Username already exists"
      
        if len(postData['alias']) < 3:
            errors['password'] = "Alias must be at least 3 characters"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = 'Email already exists'
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email_address'] = "Invalid email address!"
        if len(postData['password']) < 5:
            errors['password'] = "Password must be at least 5 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['pw_match'] = "Password must match!"
        if postData['countries'] == 'Select country':
            errors['countries'] = "You must select a country"
        return errors
            



class User(models.Model):
    username = models.CharField(max_length=120)
    alias = models.CharField(max_length=120,null=True,blank=True)
    countries = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False,blank=True)
    objects = UserManager()

