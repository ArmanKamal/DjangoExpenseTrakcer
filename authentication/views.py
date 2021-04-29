from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
# Create your views here.

class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid Email'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already exists, choose another one'},status=409)
        return JsonResponse({'email_valid':True},status=200)

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['user']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric number'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already exists, choose another one'},status=409)
        if len(username) < 3:
            return JsonResponse({'username_error':'Username should be minimum 3 characters long'},status=400)
        return JsonResponse({'username_valid':True},status=200)

class SignUpView(View):
    def get(self,request):
        return render(request,"authentication/signup.html")