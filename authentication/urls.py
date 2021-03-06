from django.urls import path
from .views import SignUpView,UsernameValidationView,EmailValidation,AliasValidationView,LoginView,LogoutView,RequestPassword,RequestPasswordCompleted,ProfilePage,EditProfilePage,UpdateProfilePage
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', SignUpView.as_view(),name="register"),
    path('login',LoginView.as_view(),name='login'),
    path('profile',ProfilePage,name='profile'),
    path('profile-edit',EditProfilePage,name='profile-edit'),
    path('profile-update',UpdateProfilePage,name='profile-update'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view())),
    path('validate-email',csrf_exempt(EmailValidation.as_view()),name="validate_email"),
    path('validate-alias',csrf_exempt(AliasValidationView.as_view()),name="validate_alias"),
    path('reset-link',RequestPassword.as_view(),name='reset-password'),
    path('set-new-password/<uid>/<token>',RequestPasswordCompleted.as_view(),name='set-new-password')
]
