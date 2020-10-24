from django.shortcuts import render
from rest_framework import viewsets
from.serializer import OrderSerializer
from .models import Order
# Create your views here.


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer