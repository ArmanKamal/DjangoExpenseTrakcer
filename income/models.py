from django.db import models
from authentication.models import User
import datetime

class IncomeManager(models.Manager):
    def income_validation(self,postData):
        errors = {}
        if not postData['amount']:
            errors['amount'] = "Please Enter the Amount."
        if len(postData['date'])<1:
            errors['date'] = "Please Choose a date"
        if postData['source'] == '':
            errors['source'] = "You must choose a source"
        if postData['source'] == 'others' and postData['source_input'] == '':
            errors['source_input'] = "You must type a source"
        source_exist = Source.objects.filter(name=postData['source_input'])
        if len(source_exist)>=1:
            errors['source_duplicate'] = "Source Already exists"
        return errors

    def income_update_validation(self,postData):
        errors = {}
        if not postData['amount']:
            errors['amount'] = "Please Enter the Amount."
        if postData['source'] == '':
            errors['source'] = "You must choose a source"
        if len(postData['date'])<1:
            errors['date'] = "Please Choose a date"
        return errors

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
    objects=IncomeManager()
    


