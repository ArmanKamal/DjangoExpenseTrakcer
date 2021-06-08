from django.shortcuts import redirect, render
from authentication.models import User
from .models import Source,Income
from usersettings.models import Setting
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    user = User.objects.filter(id=request.session['logged_user'])
    if user.count() <= 0:
        return redirect('/auth/login')
    
    incomes = Income.objects.filter(owner=user[0]).order_by('-date')
    paginator = Paginator(incomes,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    sources = Source.objects.all()
    currency = Setting.objects.get(user=user[0])
 

    context = {
        "sources": sources,
        "incomes": incomes,
        'page_obj': page_obj,
        "currency": currency
    }
    return render(request, "income.html",context)

def add_income(request):

    sources = Source.objects.all()
  
  
    context = {
        "sources": sources,
        "time": datetime.now()  
    }
 
    return render(request, "add_income.html",context)

def create_income(request):
    if request.method == "POST":
        errors = Income.objects.income_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/income/add-income')
        user = User.objects.get(id=request.session['logged_user'])
        if request.POST['source'] == "others":
            source = Source.objects.create(name=request.POST['source_input'])
        else:
            source = Source.objects.get(name=request.POST['source'])
        amount = request.POST['amount']
        description = request.POST['description']
        Income.objects.create(amount=amount, owner=user, description=description, date=request.POST['date'],source=source)
        messages.success(request,"Created successfully")
        return redirect('/income')
    
    return redirect('/income/add-income')

def edit_income(request,id):
    income = Income.objects.get(id=id)
    context = {
        "income": income,
        "sources":Source.objects.exclude(name=income.source.name)
    }
    return render(request,"edit_income.html",context)

def update_income(request, id):
    if request.method == "POST":
        errors = Income.objects.income_update_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/edit-income/{id}')
        income = Income.objects.get(id=id)
        source = Source.objects.get(name=request.POST['source'])
        income.amount = request.POST['amount']
        income.description = request.POST['description']
        income.source = source
        income.save()
        messages.success(request, "Updated Successfully")
        return redirect('/income')
    return redirect('/edit-income')