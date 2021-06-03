from django.urls import path
from .views import index,add_income,create_income

urlpatterns = [
    path('', index,name="income"),
    path('add-income', add_income,name="add-income"),
    path('create-income',create_income,name="create-income")

]
