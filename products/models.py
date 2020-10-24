from django.db import models
from categories.models import Category
from users.models import Supplier
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField(max_length=100)
    stock = models.CharField(max_length=100)
    image = models.ImageField(null = True, blank= True) # refernce https://www.youtube.com/watch?v=obZMr9URmVI
    digital = models.BooleanField(default=False,null=True,blank=True)#if its a physical product its shipped
    #category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    #supplier_id = models.ForeignKey(Supplier)

    def __str__(self):
        return self.name