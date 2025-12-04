from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('drivers/', views.drivers, name='drivers'),
    path('contacts/', views.contacts, name='contacts'),
    path('order/', views.order_taxi, name='order_taxi'),
    
    # Новые URL для оплаты и отзывов
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('reviews/', views.reviews_page, name='reviews_page'),
    path('reviews/<int:order_id>/', views.submit_review, name='submit_review'),
    
    # URL для регистрации и входа
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
]