from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=55,unique=True)
    sum = models.FloatField(default=0)
    def __str__(self):
        return self.name


class Price (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.CharField(max_length=55)
    kl = models.FloatField(default=0)
    sum = models.FloatField(default=0)
    def __str__(self):
        return self.color




