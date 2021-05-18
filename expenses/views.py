from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Category, Expense
from authentication.models import User
# Create your views here.

def index(request):
    user = User.objects.get(id=request.session['logged_user'])
    expenses = Expense.objects.filter(user=user)
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "expenses": expenses
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
        amount = request.POST['amount']
        Expense.objects.create(amount=amount, user=user,spend_date= request.POST['date'])
        messages.success(request,"Saved successfully")
        return redirect('/')
    
    return redirect('/add_expense.html')
