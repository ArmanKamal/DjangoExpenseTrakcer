from django.shortcuts import redirect, render
import json
import os
from .models import Setting
from django.contrib import messages
from django.conf import settings
from authentication.models import User
# Create your views here.
def index(request):
    currency_data = []
    path = os.path.join(settings.BASE_DIR, 'currencies.json')
    user = User.objects.get(id=request.session.get('logged_user'))
    preference_exists = Setting.objects.filter(user=user).exists()

    if preference_exists:
        user_prefrence = Setting.objects.get(user=user)
    else:
        user_prefrence = ""
    
   
    
    with open(path) as json_file:
        data = json.load(json_file)

        for key,item in data.items():
            currency_data.append({'name':key, 'value':item})
    context = {
        'currency_data': currency_data,
        'user_prefrence':user_prefrence
    }
    return render(request, 'settings/index.html',context)


def create_preference(request):
    user_prefrence = None
    user = User.objects.get(id=request.session.get('logged_user'))
    preference_exists = Setting.objects.filter(user=user).exists()

    if preference_exists:
        user_prefrence = Setting.objects.get(user=user)
    if request.method =="POST":
        user_currency = request.POST['currency']
        if preference_exists:
            user_prefrence.currency = user_currency
            user_prefrence.save()
        else:
            Setting.objects.create(user=user, currency=user_currency)     
        messages.success(request,'Saved...')
      
        return redirect('/users/settings')
    return redirect('/users/settings')