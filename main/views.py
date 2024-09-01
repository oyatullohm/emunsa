from django.shortcuts import render ,redirect
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth import authenticate, login ,logout 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
from django.db.models import Q , Sum , Case, When, Value, IntegerField
from datetime import datetime, timedelta
from django.db.models.functions import Coalesce


class HomeVIew(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        return render(request,'home.html')
    

class EmunsaView(View):
    def get(self,request):
        if request.user.is_authenticated :
            product = Product.objects.filter(type=2)
            return render(request,'index.html',{'product':product})
        return redirect('main:login')


    def post(self,request):
        if request.user.is_authenticated :
            product = request.POST.get('product')
            Product.objects.create(name=product,type=2)
            return redirect ('main:emunsa')
        return redirect('main:login')


class ProductView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        product = Product_Count.objects.filter(product__type=1)
        return render(request, 'product.html',context={'product':product})
    
    def post (self,request):
        name = request.POST.get('name')
        count = request.POST.get('soni')
        sum = request.POST.get('narhi')
        product = Product.objects.create(name=name,type=1)
        Product_Count.objects.create(product=product, count=count, sum=sum)
        return redirect ('main:tavar')
        
    

class ClientViev(LoginRequiredMixin ,View):

    login_url = '/login/'
    def get(self, request):
        type = request.GET.get('type')
        client =  Client.objects.filter(type=type)
        
        return render (request, 'client.html' ,{'client':client})
    def post(self, request):
        type = request.POST.get('type')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        amount = request.POST.get('sum')
        Client.objects.create(
            type = type,
            name= name,
            phone=phone,
            amount = amount
        )
        return redirect(f'/client/?type={type}' )

      
class OrderView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        page = request.GET.get('page')
        product = Product_Count.objects.all()
        order = Order.objects.all().order_by('-id')
        client = Client.objects.filter(type=2)
        paginator = Paginator(order, 10)
        try:
            paginated= paginator.page(page)
        except PageNotAnInteger:
            paginated= paginator.page(1)
        except EmptyPage:
            paginated= paginator.page(paginator.num_pages)
        context = {
            'client':client,
            'page_obj': paginated,
            'product':product,
        }
        return render(request, 'order.html',context)


class IncomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        page = request.GET.get('page')
        product = Product_Count.objects.all()
        income = Income.objects.all().order_by('-id')
        client = Client.objects.filter(type=1)
        paginator = Paginator(income, 10)
        try:
            paginated= paginator.page(page)
        except PageNotAnInteger:
            paginated= paginator.page(1)
        except EmptyPage:
            paginated= paginator.page(paginator.num_pages)
        context = {
            'client':client,
            'page_obj': paginated,
            'product':product,
        }
        return render(request, 'income.html',context)


class PaymentViev(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request):
        page = request.GET.get('page')

        type = request.GET.get('type')
        payment = Payment.objects.filter(type=type).order_by('-id')
        client = Client.objects.all()
        paginator = Paginator(payment, 10)
        try:
            paginated= paginator.page(page)
        except PageNotAnInteger:
            paginated= paginator.page(1)
        except EmptyPage:
            paginated= paginator.page(paginator.num_pages)
        context = {
            'page_obj': paginated,
            'client':client,
        }
        
        return render(request, 'payment.html', context)
        
    def post(self, request):
        client_id = int(request.POST.get('client'))
        amount = request.POST.get('amount')
        
        type = request.GET.get('type')

        type_ = request.POST.get('type')
        client = None
        if client_id != 0:
            client = Client.objects.get(id=client_id)
        cash = Cash.objects.last()
        payment = Payment.objects.create(
            client = client,
            type = type_,
            amount = amount,
            date = timezone.now().date(),
            cource = Cource.objects.last().cource,
            cash_before_amount = cash.amount,
        )



        if client:
           if payment.type == '1' or payment.type == 1:
                payment.client_before_amount =  client.amount
                client.amount -= float(payment.amount)
                client.save()
                payment.client_after_amount = float(client.amount)
                cash.amount += int(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount 
                payment.save()
            
           elif payment.type == '2' or payment.type == 2:
                payment.client_before_amount =  client.amount
                client.amount += float(payment.amount)
                client.save()
                payment.client_after_amount = float(client.amount)
                cash.amount -= int(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount 
                payment.save()
        else:
            if payment.type == '1' or payment.type == 1:
                cash.amount += int(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount 
                payment.save()
            elif payment.type == '2' or payment.type == 2:
                cash.amount -= int(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount 
                payment.save()
            elif payment.type == '3' or payment.type == 3:
                cash.amount -= int(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount 
                payment.save()
        return redirect(f'/payment/?type={type}' )


class CashView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        month = int(request.GET.get('month', datetime.now().month))
        year = int(request.GET.get('year', datetime.now().year))

        start_date = datetime(year, month, 1)
        next_month = start_date.replace(day=28) + timedelta(days=4)  # Keyingi oyning birinchi kuni
        end_date = next_month - timedelta(days=next_month.day)  # Tanlangan oyning oxirgi kuni

        cash = Cash.objects.last()
        totals = Payment.objects.filter(date__range=(start_date, end_date)).aggregate(
        payment=Sum(Case(When(type=1, then='amount'), default=Value(0), output_field=IntegerField())),
        payment_cost=Sum(Case(When(type=2, then='amount'), default=Value(0), output_field=IntegerField())),
        payment_=Sum(Case(When(type=3, then='amount'), default=Value(0), output_field=IntegerField()))
    )

        number_list = [ i for i in range(1,13)] 
        context = {
            'cash': cash,
            'selected_month': month,
            'selected_year': year,
            'number_list':number_list,
            "payment_cost":totals['payment_cost'] or 1,
            "payment":totals['payment']or 1,
            "payment_":totals['payment_']or 1,
        } 
        return render(request, 'cash.html', context)
        
    def post(self,request):
        amount = request.POST.get('amount')
        cahs = Cash.objects.last()
        cahs.amount = amount
        cahs.save()
      
        return  redirect('main:cash')


class SettingsView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        cource = Cource.objects.last()
        context = {
            "cource":cource
        }
        return render(request, 'settings.html', context)
    def post(self,request):
        id = request.POST.get('id')
        cource_ = request.POST.get('cource')
        cource = Cource.objects.get(id=id)
        cource.cource = cource_
        cource.date = timezone.now().date()
        cource.save()
        return redirect('main:settings')

def detail(request,pk):
    if request.user.is_authenticated :
        price =Price.objects.filter(product=pk)
        return render(request,'detail.html',{'price':price,'product_id':pk})
    return redirect('main:login')


def price_create(request,pk):
    if request.user.is_authenticated :
        product = Product.objects.get(id=int(pk))
        color = request.POST.get('rang')
        kl = request.POST.get('kl')
        sum = request.POST.get('sum')
        Price.objects.create(product=product,
                            color=color
                            ,kl=kl,
                            sum=sum)
        product_prise_all = Price.objects.filter(product=product)
        summa = float()
        for i in product_prise_all:
            summa += i.sum
        summa = summa / 30
        product.sum = summa
        product.save()

        return redirect(f'/detail/{pk}')
    return redirect('main:login')


def prise_update(request,pk):
    if request.user.is_authenticated :
        price = Price.objects.get(id=int(pk))
        color = request.POST.get('rang')
        kl = request.POST.get('kl')
        sum = request.POST.get('sum')
        price.color = color
        price.kl = kl
        price.sum = sum
        price.save()

        product= Product.objects.get( id = price.product.id)
        product_prise_all = Price.objects.filter(product=product)
        summa = float()
        for i in product_prise_all:
            summa += i.sum
        summa = summa / 30
        product.sum = summa
        product.save()
        return redirect(f'/detail/{product.id}')
    return redirect('main:login')


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')