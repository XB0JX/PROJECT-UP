
from django.shortcuts import render
from .models import Driver, Tariff

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
    
    return render(request, 'index.html', {
        'total_drivers': total_drivers,
        'available_drivers': available_drivers,
        'tariffs': active_tariffs,
        'status_stats': status_stats,
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