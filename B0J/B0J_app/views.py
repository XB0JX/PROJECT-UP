from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Driver, Tariff, PaymentMethod, Order

def index(request):
    """Главная страница с тарифами"""
    total_drivers = Driver.objects.count()
    available_drivers = Driver.objects.filter(status='available')[:3]
    active_tariffs = Tariff.objects.filter(is_active=True)
    
    status_stats = {
        'available': Driver.objects.filter(status='available').count(),
        'busy': Driver.objects.filter(status='busy').count(),
        'offline': Driver.objects.filter(status='offline').count(),
    }
    
    # Добавляем способы оплаты в контекст
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('order')[:3]
    
    return render(request, 'index.html', {
        'total_drivers': total_drivers,
        'available_drivers': available_drivers,
        'tariffs': active_tariffs,
        'status_stats': status_stats,
        'payment_methods': payment_methods,
    })

def drivers(request):
    """Страница всех водителей"""
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'all':
        all_drivers = Driver.objects.all()
    elif status_filter in ['available', 'busy', 'offline']:
        all_drivers = Driver.objects.filter(status=status_filter)
    else:
        all_drivers = Driver.objects.all()
        status_filter = 'all'
    
    return render(request, 'drivers.html', {
        'drivers': all_drivers,
        'status_filter': status_filter,
    })

def calculate_price(request):
    """Страница расчета стоимости"""
    tariffs = Tariff.objects.filter(is_active=True)
    return render(request, 'price_calc.html', {'tariffs': tariffs})

def payment_methods(request):
    """Страница со способами оплаты"""
    methods = PaymentMethod.objects.filter(is_active=True).order_by('order')
    return render(request, 'payment_methods.html', {'methods': methods})

def create_order(request):
    """Создание нового заказа"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            customer_name = request.POST.get('customer_name', '').strip()
            customer_phone = request.POST.get('customer_phone', '').strip()
            pickup_address = request.POST.get('pickup_address', '').strip()
            destination_address = request.POST.get('destination_address', '').strip()
            tariff_id = request.POST.get('tariff')
            payment_method_id = request.POST.get('payment_method')
            distance = float(request.POST.get('distance', 0))
            
            # Проверяем обязательные поля
            if not all([customer_name, customer_phone, pickup_address, destination_address, tariff_id, payment_method_id]):
                messages.error(request, 'Пожалуйста, заполните все обязательные поля')
                return redirect('create_order')
            
            # Получаем объекты
            tariff = Tariff.objects.get(id=tariff_id)
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            
            # Создаем заказ
            order = Order(
                customer_name=customer_name,
                customer_phone=customer_phone,
                pickup_address=pickup_address,
                destination_address=destination_address,
                tariff=tariff,
                payment_method=payment_method,
                distance=distance,
                estimated_time=int(distance * 5)  # Примерный расчет времени
            )
            
            # Рассчитываем цену
            order.calculate_price()
            
            # Автоматически назначаем свободного водителя с подходящим тарифом
            available_driver = Driver.objects.filter(
                status='available',
                available_tariffs=tariff
            ).first()
            
            if available_driver:
                order.driver = available_driver
                available_driver.status = 'busy'
                available_driver.save()
                order.status = 'accepted'
            else:
                order.status = 'pending'
            
            order.save()
            
            # Сообщение об успехе
            messages.success(request, f'Заказ #{order.id} успешно создан! Стоимость: {order.total_price}₽')
            return redirect('index')
            
        except Tariff.DoesNotExist:
            messages.error(request, 'Выбранный тариф не найден')
        except PaymentMethod.DoesNotExist:
            messages.error(request, 'Выбранный способ оплаты не найден')
        except Exception as e:
            messages.error(request, f'Ошибка при создании заказа: {str(e)}')
    
    # GET запрос - показываем форму
    tariffs = Tariff.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'order_payment.html', {
        'tariffs': tariffs,
        'payment_methods': payment_methods,
    })

def order_history(request):
    """История заказов"""
    orders = Order.objects.all().order_by('-created_at')[:10]
    return render(request, 'order_history.html', {'orders': orders})