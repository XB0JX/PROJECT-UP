from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Driver, Customer, Order, Payment, Review
import random

def index(request):
    """Главная страница"""
    try:
        available_drivers = Driver.objects.filter(is_available=True)
        total_drivers = Driver.objects.count()
        total_orders = Order.objects.count()
        
        # Получаем последние отзывы
        latest_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:3]
    except:
        available_drivers = []
        total_drivers = 0
        total_orders = 0
        latest_reviews = []
    
    return render(request, 'index.html', {
        'available_drivers': available_drivers,
        'total_drivers': total_drivers,
        'total_orders': total_orders,
        'latest_reviews': latest_reviews,
    })

def about(request):
    return render(request, 'about.html')

def drivers(request):
    try:
        drivers_list = Driver.objects.all()
    except:
        drivers_list = []
    return render(request, 'drivers.html', {'drivers': drivers_list})

def contacts(request):
    return render(request, 'contacts.html')

def order_taxi(request):
    """Обработка заказа такси"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        destination = request.POST.get('destination')
        payment_method = request.POST.get('payment_method', 'cash')
        
        if name and phone and address:
            try:
                # Ищем или создаем клиента
                customer, created = Customer.objects.get_or_create(
                    phone=phone,
                    defaults={'total_orders': 0, 'total_spent': 0}
                )
                
                # Генерируем примерную стоимость
                price = round(random.uniform(200, 1500), 2)
                
                # Создаем заказ
                order = Order.objects.create(
                    customer=customer,
                    customer_name=name,
                    customer_phone=phone,
                    pickup_address=address,
                    destination=destination or "Не указано",
                    payment_method=payment_method,
                    price=price,
                    distance=round(random.uniform(2, 20), 1),
                    estimated_time=random.randint(10, 60)
                )
                
                # Пытаемся найти свободного водителя
                available_driver = Driver.objects.filter(is_available=True).first()
                if available_driver:
                    order.driver = available_driver
                    order.status = 'accepted'
                    order.save()
                    
                    # Обновляем статус водителя
                    available_driver.is_available = False
                    available_driver.save()
                
                # Создаем запись о платеже
                Payment.objects.create(
                    order=order,
                    amount=price,
                    payment_method=payment_method,
                    status='pending'
                )
                
                # Обновляем статистику клиента
                customer.total_orders += 1
                customer.total_spent += price
                customer.save()
                
                # Перенаправляем на страницу оплаты
                return redirect(f'/payment/{order.id}/')
                
            except Exception as e:
                return redirect('/?order=error')
    
    return redirect('/')

def payment_page(request, order_id):
    """Страница оплаты"""
    order = get_object_or_404(Order, id=order_id)
    payment = Payment.objects.filter(order=order).first()
    
    return render(request, 'payment.html', {
        'order': order,
        'payment': payment,
    })

def process_payment(request, order_id):
    """Обработка платежа"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        payment = Payment.objects.filter(order=order).first()
        
        if payment:
            payment.status = 'completed'
            payment.transaction_id = f"TXN{random.randint(100000, 999999)}"
            payment.save()
            
            order.status = 'completed'
            order.save()
            
            # Освобождаем водителя
            if order.driver:
                order.driver.is_available = True
                order.driver.save()
        
        return redirect(f'/reviews/{order.id}/')
    
    return redirect('/')

def reviews_page(request):
    """Страница всех отзывов"""
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})

def submit_review(request, order_id):
    """Отправка отзыва"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment and order.driver:
            Review.objects.create(
                customer=order.customer,
                driver=order.driver,
                order=order,
                rating=int(rating),
                comment=comment
            )
            
            # Обновляем рейтинг водителя
            driver_reviews = Review.objects.filter(driver=order.driver)
            if driver_reviews:
                avg_rating = sum(r.rating for r in driver_reviews) / driver_reviews.count()
                order.driver.rating = round(avg_rating, 1)
                order.driver.save()
        
        return redirect('/reviews/')
    
    return render(request, 'submit_review.html', {'order_id': order_id})

def register(request):
    """Регистрация клиента"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if username and email and phone and password:
            try:
                user = User.objects.create_user(username, email, password)
                customer = Customer.objects.create(user=user, phone=phone)
                login(request, user)
                return redirect('/')
            except:
                return redirect('/?register=error')
    
    return render(request, 'register.html')

def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
    
    return render(request, 'login.html')

def profile(request):
    """Профиль клиента"""
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    try:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-order_time')
        reviews = Review.objects.filter(customer=customer)
    except Customer.DoesNotExist:
        customer = None
        orders = []
        reviews = []
    
    return render(request, 'profile.html', {
        'customer': customer,
        'orders': orders,
        'reviews': reviews,
    })