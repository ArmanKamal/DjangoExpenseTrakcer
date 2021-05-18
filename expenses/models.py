from django.db import models
import datetime

from authentication.models import User


class ExpenseManager(models.Manager):
    def expense_validation(self,postData):
        errors = {}
        if not postData['amount']:
            errors['amount'] = "Please Enter the Amount."
        if len(postData['date'])<1:
            errors['date'] = "Please Choose a date"
        return errors
            

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    spend_date = models.DateField(default=datetime.date.today())
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    category = models.ManyToManyField("Category",null=True)
    creted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExpenseManager()
class Category(models.Model):
    name = models.CharField(max_length=255)
    creted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)