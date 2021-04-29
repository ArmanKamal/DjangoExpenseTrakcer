from django.urls import path
from .views import SignUpView,UsernameValidationView,EmailValidation
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', SignUpView.as_view(),name="register"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view())),
    path('validate-email',csrf_exempt(EmailValidation.as_view()),name="validate_email")
    
]
