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

        order = Order.objects.create(
            date = timezone.now().date(),
            client = client,
            cource = 12650,
            
        )
        for i in products:
            item = OrderItem.objects.create(
                product = Product_Count.objects.get(id=int(i['product'])),
                count = i['count'],
                price = i['price']
            )
            prduct_count = item.product
            prduct_count -= item.count
            prduct_count.save()
            order.items.add(item)
            order.save()
        
        if order.client:
            if isNasyaChecked:
                client.amount += order.total_summa
                client.save()  
            elif not isNasyaChecked :
                Payment.objects.create(
                    client = client,
                    type = 1,
                    date = timezone.now().date(),
                    amount = order.total_summa
                )
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)