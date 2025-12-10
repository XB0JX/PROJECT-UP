from django.contrib import admin
from .models import Tariff, Driver, PaymentMethod, Order

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'price_per_km', 'price_per_minute', 'is_active']
    list_filter = ['is_active', 'name']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_model', 'car_number', 'phone', 'rating', 'status']
    list_filter = ['status', 'has_child_seat', 'has_cargo_space']
    search_fields = ['name', 'car_model', 'car_number', 'phone']
    list_editable = ['status']
    filter_horizontal = ['available_tariffs']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'tariff', 'driver', 'total_price', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'tariff', 'payment_method']
    search_fields = ['customer_name', 'customer_phone', 'pickup_address', 'destination_address']
    list_editable = ['status', 'is_paid']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'commission', 'min_amount', 'max_amount', 'order']
    list_editable = ['is_active', 'commission', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    
    # Автоматическое заполнение иконки
    def save_model(self, request, obj, form, change):
        if not obj.icon:
            obj.icon = obj.get_icon()
        super().save_model(request, obj, form, change)