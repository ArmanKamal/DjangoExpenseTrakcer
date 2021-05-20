from django.urls import path
from .views import index,add_expense,create_expense,edit_expense,delete_expense,update_expense

urlpatterns = [
    path('', index,name="home"),
    path('add-expense', add_expense,name="add-expense"),
    path('create-expense', create_expense,name="create-expense"),
    path('edit-expense/<int:id>', edit_expense,name="edit-expense"),
    path('update-expense/<int:id>', update_expense,name="update-expense"),
    path('delete-expense/<int:id>',delete_expense,name="delete-expense")
]
