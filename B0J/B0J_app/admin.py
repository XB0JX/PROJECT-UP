from django.contrib import admin
from .models import Driver, Customer, Order, Payment, Review

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'car_number', 'phone', 'rating', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'car_model', 'car_number', 'phone')
    list_editable = ('is_available',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'registration_date', 'total_orders', 'total_spent')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('registration_date',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'driver', 'status', 'payment_method', 'price', 'order_time')
    list_filter = ('status', 'payment_method')
    search_fields = ('customer_name', 'customer_phone', 'pickup_address', 'destination')
    readonly_fields = ('order_time',)
    list_editable = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'payment_method', 'status', 'payment_time')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'order__id')
    readonly_fields = ('payment_time',)
    list_editable = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'driver', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved')
    search_fields = ('comment', 'customer__user__username')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)