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
        if postData['category'] == '':
            errors['category'] = "You must choose a category"
        if postData['category'] == 'others' and postData['category_input'] == '':
            errors['category_input'] = "You must type a category"
        category_exist = Category.objects.filter(name=postData['category_input'])
        if len(category_exist)>=1:
            errors['category_duplicate'] = "Category Already exists"
        return errors

    def expense_update_validation(self,postData):
        errors = {}
        if not postData['amount']:
            errors['amount'] = "Please Enter the Amount."
        if postData['category'] == '':
            errors['category'] = "You must choose a category"
   
        return errors


class Category(models.Model):
    name = models.CharField(max_length=255)
    creted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)       

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    spend_date = models.DateField(default=datetime.date.today())
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey(Category, null=True,on_delete=models.CASCADE)
    creted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExpenseManager()
