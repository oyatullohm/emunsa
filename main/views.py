from django.shortcuts import render ,redirect
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product , Price
from django.contrib.auth import authenticate, login ,logout 

class HomeVIew(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        return render(request,'home.html')
    

class EmunsaView(View):
    def get(self,request):
        if request.user.is_authenticated :
            product = Product.objects.all()
            return render(request,'index.html',{'product':product})
        return redirect('main:login')


    def post(self,request):
        if request.user.is_authenticated :
            product = request.POST.get('product')
            Product.objects.create(name=product)
            return redirect ('main:home')
        return redirect('main:login')
    
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

class ClientViev(LoginRequiredMixin ,View):
    login_url = '/login/'
    def get(self, request):
        return render (request, 'client.html')