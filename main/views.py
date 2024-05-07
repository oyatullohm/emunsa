from django.shortcuts import render ,redirect
from django.views import View
from .models import Product , Price
from django.contrib.auth import authenticate, login ,logout
from .decorator import deco_login

class HomeView(View):
    # @deco_login
    def get(self,request):
        product = Product.objects.all()
        return render(request,'index.html',{'product':product})
    # @deco_login
    def post(self,request):
        product = request.POST.get('product')
        Product.objects.create(name=product)
        return redirect ('main:home')

# @deco_login
def detail(request,pk):
    price =Price.objects.filter(product=pk)
    return render(request,'detail.html',{'price':price,'product_id':pk})


# @deco_login
def price_create(request,pk):
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


# @deco_login
def prise_update(request,pk):
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