from django.db import models
from users.models import Customer
# Create your models here.


class Order(models.Model):
    deliverystatus = models.CharField(max_length=12)
    quantity = models.CharField(max_length=10)
    orderdate = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)#it means its an open cart
    transaction_id = models.AutoField(primary_key=True)
    

    
    def __str__(self): 
        return self.deliverystatus


#this is the cart 
class OrderItem(models.Model):
    quanity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
   


class ShippingAddress(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    date_added = models.DateField(auto_now_add=True)
