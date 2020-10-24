from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['deliverystatus', 'quantity', 'orderdate', 'complete', 'transaction_id']