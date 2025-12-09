from django.contrib import admin
from .models import Driver, Tariff

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'base_price', 'price_per_km', 'price_per_minute', 'is_active']
    list_filter = ['name', 'is_active']
    list_editable = ['is_active', 'base_price', 'price_per_km']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_model', 'car_number', 'status', 'rating', 'has_child_seat', 'has_cargo_space']
    list_filter = ['status', 'has_child_seat', 'has_cargo_space', 'available_tariffs']
    list_editable = ['status', 'has_child_seat', 'has_cargo_space']
    filter_horizontal = ['available_tariffs']
    search_fields = ['name', 'car_model', 'car_number']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'car_model', 'car_number', 'phone', 'rating', 'experience')
        }),
        ('Специальные возможности', {
            'fields': ('has_child_seat', 'has_cargo_space', 'max_passengers')
        }),
        ('Тарифы и статус', {
            'fields': ('available_tariffs', 'status')
        }),
    )