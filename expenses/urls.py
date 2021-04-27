from django.urls import path
from .views import index,add_expense

urlpatterns = [
    path('', index,name="home"),
    path('add-expense', add_expense,name="home"),
]
