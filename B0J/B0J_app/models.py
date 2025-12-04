from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Driver(models.Model):
    """Модель водителя такси"""
    name = models.CharField(max_length=100, verbose_name="Имя водителя")
    car_model = models.CharField(max_length=50, verbose_name="Модель автомобиля")
    car_number = models.CharField(max_length=15, verbose_name="Номер автомобиля")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    rating = models.FloatField(default=5.0, verbose_name="Рейтинг")
    experience = models.IntegerField(default=1, verbose_name="Стаж (лет)")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    photo = models.CharField(max_length=200, default="🚗", verbose_name="Фото (эмодзи)")
    
    def __str__(self):
        return f"{self.name} - {self.car_model} ({self.car_number})"
    
    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

class Customer(models.Model):
    """Модель клиента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон", unique=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    total_orders = models.IntegerField(default=0, verbose_name="Всего заказов")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Всего потрачено")
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Гость'} - {self.phone}"
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Order(models.Model):
    """Модель заказа такси"""
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принят'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', '💵 Наличные'),
        ('card', '💳 Карта водителю'),
        ('online_card', '💻 Карта онлайн'),
        ('apple_pay', '📱 Apple Pay'),
        ('google_pay', '📱 Google Pay'),
        ('yandex_money', '💰 Яндекс.Деньги'),
        ('sberbank', '🏦 Сбербанк Онлайн'),
        ('qiwi', '🥝 QIWI'),
        ('corporate', '🏢 Корпоративный счет'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент", null=True, blank=True)
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    pickup_address = models.TextField(verbose_name="Адрес подачи")
    destination = models.TextField(verbose_name="Адрес назначения")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Водитель")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash', verbose_name="Способ оплаты")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость")
    distance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Расстояние (км)")
    estimated_time = models.IntegerField(default=0, verbose_name="Примерное время (мин)")
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.customer_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_time']

class Payment(models.Model):
    """Модель платежа"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('processing', 'В обработке'),
        ('completed', 'Оплачено'),
        ('failed', 'Не удалось'),
        ('refunded', 'Возврат'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_method = models.CharField(max_length=20, choices=Order.PAYMENT_METHODS, verbose_name="Способ оплаты")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID транзакции")
    payment_time = models.DateTimeField(auto_now_add=True, verbose_name="Время платежа")
    notes = models.TextField(blank=True, verbose_name="Примечания")
    
    def __str__(self):
        return f"Платеж #{self.id} - {self.amount} руб."
    
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

class Review(models.Model):
    """Модель отзыва"""
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент", null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен")
    
    def __str__(self):
        return f"Отзыв от {self.customer.user.username if self.customer and self.customer.user else 'Гость'}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']