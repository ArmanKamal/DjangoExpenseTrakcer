from django.urls import path
from .views import index,add_income,create_income,edit_income,update_income,search_income,delete_income

urlpatterns = [
    path('', index,name="income"),
    path('add-income', add_income,name="add-income"),
    path('create-income',create_income,name="create-income"),
    path('edit-income/<int:id>',edit_income,name="edit-income"),
    path('update-income/<int:id>', update_income,name="update-income"),
    path('delete-income/<int:id>',delete_income,name="delete-income"),
    path('search',search_income,name="search-income")

]
