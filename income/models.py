from django.db import models
from authentication.models import User
import datetime


class Source(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=datetime.date.today())
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Source,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


