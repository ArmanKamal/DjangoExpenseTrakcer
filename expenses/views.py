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
        category = Category.objects.get(name=request.POST['category'])
        amount = request.POST['amount']
        expense =Expense.objects.create(amount=amount, user=user,spend_date= request.POST['date'],category=category )
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
    pass

