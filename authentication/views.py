import re
from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from .models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
import bcrypt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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

        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('activate',kwargs={'uid':uid,'token':token_generator.make_token(user)})
        email_body = f'Please use this link to activate your account\nhttp://{domain+link}'
        email_message = send_mail(
            'Activate Your account',
            email_body ,
            'noreply@abc.com',
            [email],
            
        )
        messages.success(request,"Please check your email to activate the account")
        return redirect('/auth/login')
        
   

class VerificationView(View):
    def get(self,request,uid, token):
        try:
            id = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not token_generator.check_token(user, token):
                return redirect('/auth/login'+'?messages='+'User already activated')
            
            if user.is_active:
                request.session['logged_user'] = user.id
                messages.success('Account has been activated')
                return redirect('/auth/login')
            user.is_active = True
            user.save()
        except Exception as e:
            pass
        return redirect('/auth/login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/signin.html')

    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email)

        if not email and not password:
            messages.error(request, "Please enter your email and password")
            return redirect('/auth/login')
        if user:
            logged_user = user[0]

            if bcrypt.checkpw(password.encode(),logged_user.password.encode()):
                if logged_user.is_active:
                    request.session['logged_user'] = logged_user.id
                    return redirect('/')
                else:
                    messages.error(request, "Account is not activate, Please check your email")
                    return redirect('/auth/login')
        messages.error(request, "Email or password are incorrect")

        return redirect('/auth/login')

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        messages.success(request,'You have been logout')
        return redirect('/auth/login')

class RequestPassword(View):
    def get(self,request):
        return render(request, 'authentication/reset-password.html')

    def post(self,request):
        email = request.POST['email']
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'authentication/reset-password.html')
        
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
     
        if user.exists() and user[0].is_active:
            print(user[0])
            uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse('set-new-password',kwargs={'uid':uid,'token':token_generator.make_token(user[0])})
            email_body = f'Please click the link to reset your account password\nhttp://{domain+link}'
            email_message = send_mail(
                'Reset Password',
                email_body ,
                'noreply@abc.com',
                [email],
                
            )
            messages.success(request,"We have sent to an email to reset your password")
            return redirect('/auth/reset-link')
        else:
            messages.error(request,'Please activate your account first.See your previous email')
            return redirect('/auth/login')


class RequestPasswordCompleted(View):
    def get(self,request,uid,token):
        context = {
            'uid':uid,
            'token':token
        }
        user_id = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(id=user_id)
  
        if not token_generator.check_token(user,token):
            messages.error(request,'Password link is invalid, please request a new one')
            return redirect('/auth/reset-link')
        return render(request,"authentication/set-newpassword.html",context)

    def post(self,request,uid,token):
        context = {
                'uid':uid,
                'token':token
            }
        if request.method == "POST":
            password = request.POST['password']
            confirm_pw = request.POST['confirm_pw']

            if len(password) <= 5:
                messages.error(request,'Password field must be atleast 6 characters')
                return render(request,"authentication/set-newpassword.html",context)
            if password != confirm_pw:
                messages.error(request,"Password and confirm password doesnot match")
                return render(request,"authentication/set-newpassword.html",context)
            user_id = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.password = hash_pw
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('/auth/login')
        return render(request,"authentication/set-newpassword.html",context)

          

