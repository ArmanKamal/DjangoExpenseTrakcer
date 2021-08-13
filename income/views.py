from django.shortcuts import redirect, render
from authentication.models import User
from .models import Source,Income
from usersettings.models import Setting
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse, response
from django.db.models import Q
import csv
# Create your views here.
def index(request):
    if 'logged_user' not in request.session:
        messages.error('Login required')
        return redirect('/auth/login')
    user = User.objects.filter(id=request.session['logged_user'])
    if user.count() <= 0:
        return redirect('/auth/login')
    
    incomes = Income.objects.filter(owner=user[0]).order_by('-date')
    paginator = Paginator(incomes,20)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    sources = Source.objects.all()
    currency = Setting.objects.filter(user=user[0])
    if currency.exists():
        user_currecy = currency[0]
    else:
        user_currecy = {
            "USD":"USD"
        }
 

    context = {
        "sources": sources,
        "incomes": incomes,
        'page_obj': page_obj,
        "currency": user_currecy
    }
    return render(request, "income.html",context)

def add_income(request):
    if 'logged_user' not in request.session:
        messages.error('Login required')
        return redirect('/auth/login')
    sources = Source.objects.all()
  
  
    context = {
        "sources": sources,
        "time": datetime.date.today()  
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
    if 'logged_user' not in request.session:
        messages.error('Login required')
        return redirect('/auth/login')
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
        income.date = request.POST['date']
        income.source = source
        income.save()
        messages.success(request, "Updated Successfully")
        return redirect('/income')
    return redirect('/edit-income')


def delete_income(request,id):
        if 'logged_user' not in request.session:
            messages.error('Login required')
            return redirect('/auth/login')
        income = Income.objects.get(id=id)
        income.delete()
        messages.success(request,'Deleted Successfully')
        return redirect('/income')




def search_income(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search')
        user = User.objects.get(id=request.session['logged_user'])
        lookups = Q(amount__istartswith=search,owner=user) | Q(date__istartswith=search,owner=user) |  Q(description__icontains=search,owner=user) |  Q(source__name__icontains=search,owner=user)
        incomes = Income.objects.filter(lookups)
        data = list(incomes.values())
        for d in data:
            source = Source.objects.get(id=d['source_id'])
            d['source_id'] = source.name
        return JsonResponse(data, safe=False)


def income_summary(request):
    current_date = datetime.date.today()
    user = User.objects.get(id=request.session['logged_user'])
    six_month_prev_date =current_date-datetime.timedelta(days=180)
    incomes = Income.objects.filter(owner=user,date__gte=six_month_prev_date,date__lte=current_date)
    final = {}
    def get_category(incomes):
        return incomes.source.name

    category_list = list(set(map(get_category,incomes)))
    def get_income_source_amount(source):
        amount = 0
        filter_incomes =incomes.filter(source__name=source)
        for x in filter_incomes:
            amount += x.amount
        return amount

    for x in incomes:
        for y in category_list:
            final[y] = get_income_source_amount(y)
    return JsonResponse({'income_source_data': final},safe=False)



def income_summary_one_month(request):
    current_date = datetime.date.today()
    user = User.objects.get(id=request.session['logged_user'])
    income_summary_one_month =current_date-datetime.timedelta(days=180)
    incomes = Income.objects.filter(owner=user,date__gte=income_summary_one_month,date__lte=current_date)
    final = {}
    def get_category(incomes):
        return incomes.source.name

    category_list = list(set(map(get_category,incomes)))
    def get_income_source_amount(source):
        amount = 0
        filter_incomes =incomes.filter(source__name=source)
        for x in filter_incomes:
            amount += x.amount
        return amount

    for x in incomes:
        for y in category_list:
            final[y] = get_income_source_amount(y)
    return JsonResponse({'income_source_data': final},safe=False)

def income_stats_view(request):
    if 'logged_user' not in request.session:
        return redirect('/auth/login')
    return render(request, 'income_summary.html')

def income_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition']='attatchment; filename=Incomes'+str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date'])
    user = User.objects.get(id=request.session['logged_user'])
    incomes = Income.objects.filter(owner=user)

    for income in incomes:
         writer.writerow([income.amount,income.description,income.source.name,income.date])

    return response