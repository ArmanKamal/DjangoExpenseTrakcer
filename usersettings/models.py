from django.db import models
from authentication.models import User
# Create your models here.
class Setting(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    currency = models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        return str(user)
