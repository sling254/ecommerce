from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ProductSerializer
from .models import Product
# Create your views here.


class ProductView(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing products instances.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
   

