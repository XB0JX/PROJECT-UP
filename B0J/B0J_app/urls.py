# B0J_app/urls.py
from django.urls import path
from . import views  # Импорт из текущей папки B0J_app

urlpatterns = [
    path('', views.index, name='index'),
    path('drivers/', views.drivers, name='drivers'),
    path('calculate/', views.calculate_price, name='calculate_price'),
    path('order/', views.create_order, name='create_order'),
    path('payment-methods/', views.payment_methods, name='payment_methods'),
]