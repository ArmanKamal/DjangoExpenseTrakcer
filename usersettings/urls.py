from django.urls import path
from .views import index,create_preference
urlpatterns = [
    path('settings',index,name="settings"),
    path('settings/create',create_preference,name="settings-create")
]
