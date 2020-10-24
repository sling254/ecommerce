from django.urls import path, include
from rest_framework import routers
from .views import OrderView


router = routers.DefaultRouter()
router.register('order', OrderView)

urlpatterns = [
    path('api/', include(router.urls))
]
