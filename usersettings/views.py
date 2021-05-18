from django.shortcuts import render
import json
import os
from django.conf import settings
# Create your views here.
def index(request):
    currency_data = []
    path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(path) as json_file:
        data = json.load(json_file)

        for key,item in data.items():
            currency_data.append({'name':key, 'value':item})
    context = {
        'currency_data': currency_data
    }

    return render(request, 'settings/index.html')