from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drivers/', views.drivers, name='drivers'),
    path('calculate/', views.calculate_price, name='calculate_price'),
]