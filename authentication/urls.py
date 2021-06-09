from django.urls import path
from .views import SignUpView,UsernameValidationView,EmailValidation,AliasValidationView,VerificationView,LoginView,LogoutView,RequestPassword,RequestPasswordCompleted
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', SignUpView.as_view(),name="register"),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view())),
    path('validate-email',csrf_exempt(EmailValidation.as_view()),name="validate_email"),
    path('validate-alias',csrf_exempt(AliasValidationView.as_view()),name="validate_alias"),
    path('activate/<uid>/<token>', VerificationView.as_view(),name='activate'),
    path('reset-link',RequestPassword.as_view(),name='reset-password'),
    path('set-new-password',RequestPasswordCompleted.as_view(),name='setNew-password')
]
