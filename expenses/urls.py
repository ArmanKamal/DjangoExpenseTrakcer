from django.urls import path
from .views import index,add_expense,create_expense

urlpatterns = [
    path('', index,name="home"),
    path('add-expense', add_expense,name="add-expense"),
    path('create-expense', create_expense,name="create-expense"),
]
