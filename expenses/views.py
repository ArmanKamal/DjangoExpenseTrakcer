from django.contrib import messages
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Category, Expense
from authentication.models import User
from django.db.models import Q
import json
from django.http import JsonResponse
from usersettings.models import Setting
# Create your views here.

def index(request):
    if 'logged_user' not in request.session:
        return redirect('/auth/login')
    user = User.objects.get(id=request.session['logged_user'])
    expenses = Expense.objects.filter(user=user).order_by('-spend_date')
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    categories = Category.objects.all()
    
    currency = Setting.objects.filter(user=user)
    if currency.exists():
        user_currecy = currency[0]
    else:
        user_currecy = {
            "USD":"USD"
        }

    

    context = {
        "categories": categories,
        "expenses": expenses,
        'page_obj': page_obj,
        "currency": user_currecy
    }
    return render(request, "index.html",context)


def add_expense(request):
    categories = Category.objects.all()
  
    context = {
        "categories": categories,
       
    }
    return render(request, "add_expense.html",context)

def create_expense(request):
    if request.method == "POST":
        errors = Expense.objects.expense_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/add-expense')
        user = User.objects.get(id=request.session['logged_user'])
        if request.POST['category'] == "others":
            category = Category.objects.create(name=request.POST['category_input'])
        else:
            category = Category.objects.get(name=request.POST['category'])
        amount = request.POST['amount']
        Expense.objects.create(amount=amount, user=user,spend_date= request.POST['date'],category=category )
        messages.success(request,"Saved successfully")
        return redirect('/')
    
    return redirect('/add_expense.html')


def edit_expense(request,id):
    context = {

        "expense": Expense.objects.get(id=id),
         "categories":Category.objects.all()
    }
    return render(request, "edit_expense.html",context)

def update_expense(request,id):
    if request.method == "POST":
        errors = Expense.objects.expense_update_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/edit-expense/{id}')
        expense = Expense.objects.get(id=id)
        category = Category.objects.get(name=request.POST['category'])
        expense.amount = request.POST['amount']
        expense.description = request.POST['description']
        expense.category = category
        expense.save()
        messages.success(request, "Updated Successfully")
        return redirect('/')
    return redirect('/edit-expense')

def delete_expense(request,id):
        expense = Expense.objects.get(id=id)
        expense.delete()
        messages.success(request,'Deleted Successfully')
        return redirect('/')




def search_expenses(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search')
        user = User.objects.get(id=request.session['logged_user'])
        lookups = Q(amount__istartswith=search,user=user) | Q(spend_date__istartswith=search,user=user) |  Q(description__icontains=search,user=user) |  Q(category__name__icontains=search,user=user)
        expenses = Expense.objects.filter(lookups)
        data = list(expenses.values())
        for d in data:
            category = Category.objects.get(id=d['category_id'])
            d['category_id'] = category.name
        return JsonResponse(data, safe=False)
