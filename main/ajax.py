from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *# Import qilingan modellaringiz
import json


@csrf_exempt  
def save_data(request):
    if request.method == 'POST':
        client_id = int( request.POST.get('client'))
        isNasyaChecked = request.POST.get('isNasyaChecked')
        client = None
        if client_id !=0 :
            client = Client.objects.get(id=client_id)
  
        products = json.loads(request.POST.get('products'))
        cource = Cource.objects.last()
        order = Order.objects.create(
            date = timezone.now().date(),
            client = client,
            cource = cource.cource,
            loan = isNasyaChecked == 'true'
        )
        for i in products:
            item = OrderItem.objects.create(
                product = Product_Count.objects.get(id=int(i['product'])),
                count = int(i['count']),
                price = i['price']
            )
            prduct_count = item.product
            prduct_count.count -= item.count
            prduct_count.save()
            order.items.add(item)   
            order.save()

            
        if order.client:
            
            if isNasyaChecked== 'true':
                order.client_before = client.amount
                client.amount += order.total_summa
                client.save()  
                order.client_after = client.amount
                order.save()
            elif isNasyaChecked == 'false':
                order.client_before = client.amount
                order.client_after = client.amount
                order.save()
                payment = Payment.objects.create(
                    client = client,
                    type = 1,
                    date = timezone.now().date(),
                    amount = order.total_summa,
                    cource = cource.cource,
                    client_before_amount = client.amount,
                    client_after_amount = client.amount,
                    
                )
                cash = Cash.objects.last()
                payment.cash_before_amount = cash.amount
                cash.amount += float(payment.amount)
                cash.save()
                payment.cash_after_amount = cash.amount
                payment.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)