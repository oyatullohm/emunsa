from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=55,unique=True)
    sum = models.FloatField(default=0)
    def __str__(self):
        return self.name


class Price (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='prices')
    color = models.CharField(max_length=55)
    sum = models.FloatField(default=0)
    kl = models.FloatField(default=0)
    def __str__(self):
        return self.color


class Product_Count(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='counts')
    count = models.PositiveIntegerField(default=0)

class Client(models.Model):
    TYPE= (
        (1,"Taminotchi"),
        (2,"Haridor")
    )
    type = models.IntegerField(choices=TYPE , default=2)
    phone = models.CharField(max_length=55)
    name = models.CharField(max_length=55)
    amount = models.FloatField(default=0)
    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    TYPE = (
        (1,"Kirim"),
        (2,"Chiqim")
    )
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, blank=True)
    type = models.IntegerField(choices=TYPE, default=1)
    client_before_amount = models.FloatField(default=0)
    client_after_amount = models.FloatField(default=0)
    cash_before_amount = models.FloatField(default=0)
    cash_after_amount = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    amount = models.FloatField(default=0)
    def __str__(self) -> str:
        return f"{self.amount}"


class Cash(models.Model):
    amount = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return f"{self.amount}"



