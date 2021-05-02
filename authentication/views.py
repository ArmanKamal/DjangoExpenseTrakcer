from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from .models import User
from validate_email import validate_email
from django.contrib import messages
import bcrypt
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

class AliasValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        alias = data['alias']
        if len(alias) < 3:
            return JsonResponse({'alias_error':'Alias should be minimum 3 characters long'},status=400)
        return JsonResponse({'alias_valid':True},status=200)

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

    def post(self,request):
        errors = User.objects.regsiter_validation(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/auth/register')
        username = request.POST['username']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        countries = request.POST['countries']

        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(username=username, email=email, alias=alias,password=hash_pw,countries=countries)
        print(user)
        return redirect('/')
        
   

