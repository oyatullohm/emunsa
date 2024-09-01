from django.shortcuts import render ,redirect
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth import authenticate, login ,logout 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
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
        paginator = Paginator(order, 2)
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

        