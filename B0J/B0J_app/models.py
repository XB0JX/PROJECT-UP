from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Tariff(models.Model):
    """Модель тарифа такси"""
    TARIFF_TYPES = [
        ('economy', '🚗 Эконом'),
        ('comfort', '🚙 Комфорт'),
        ('business', '🏎️ Бизнес'),
        ('premium', '⭐ Премиум'),
        ('cargo', '🚚 Грузовой'),
        ('family', '👨‍👩‍👧‍👦 С детьми'),
    ]
    
    name = models.CharField(max_length=20, choices=TARIFF_TYPES, verbose_name="Тип тарифа")
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Базовая цена (₽)")
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена за км (₽)")
    price_per_minute = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена за минуту (₽)")
    description = models.TextField(verbose_name="Описание", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    icon = models.CharField(max_length=10, default="🚗", verbose_name="Иконка")
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.base_price}₽"
    
    def get_features(self):
        """Возвращает список преимуществ тарифов"""
        features = {
            'economy': ["Недорого", "Быстро", "Базовые условия"],
            'comfort': ["Комфорт", "Чистый салон", "Водитель с опытом"],
            'business': ["VIP-обслуживание", "Премиум автомобиль", "Вода в салоне"],
            'premium': ["Лучшие автомобили", "Личный водитель", "Максимальный комфорт"],
            'cargo': ["Перевозка грузов", "Просторный багажник", "Помощь с погрузкой"],
            'family': ["Детское кресло", "Безопасная езда", "Игрушки для детей"],
        }
        return features.get(self.name, ["Стандартные условия"])
    
    def get_extra_info(self):
        """Дополнительная информация для тарифов"""
        info = {
            'cargo': "Автомобили с большим багажником или микроавтобусы",
            'family': "Автомобили оборудованные детскими креслами",
            'economy': "Бюджетный вариант для коротких поездок",
            'comfort': "Идеально для деловых встреч",
            'business': "Для важных переговоров и встреч",
            'premium': "Максимум комфорта и приватности",
        }
        return info.get(self.name, "")
    
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ['base_price']


class Driver(models.Model):
    """Модель водителя такси"""
    STATUS_CHOICES = [
        ('available', '🟢 Свободен'),
        ('busy', '🔴 Занят'),
        ('offline', '⚫ Не в сети'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя водителя")
    car_model = models.CharField(max_length=50, verbose_name="Модель автомобиля")
    car_number = models.CharField(max_length=15, verbose_name="Номер авто")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    rating = models.FloatField(default=5.0, verbose_name="Рейтинг")
    experience = models.IntegerField(default=1, verbose_name="Стаж (лет)")
    
    has_child_seat = models.BooleanField(default=False, verbose_name="Есть детское кресло")
    has_cargo_space = models.BooleanField(default=False, verbose_name="Большой багажник")
    max_passengers = models.IntegerField(default=4, verbose_name="Макс. пассажиров")
    
    available_tariffs = models.ManyToManyField(Tariff, verbose_name="Доступные тарифы", blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="Статус"
    )
    
    def __str__(self):
        return f"{self.name} - {self.car_model}"
    
    def get_special_features(self):
        """Возвращает специальные возможности водителя"""
        features = []
        if self.has_child_seat:
            features.append("👶 Детское кресло")
        if self.has_cargo_space:
            features.append("📦 Большой багажник")
        if self.max_passengers > 4:
            features.append(f"👥 До {self.max_passengers} пассажиров")
        return features
    
    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ['-rating']


class PaymentMethod(models.Model):
    """Модель способа оплаты"""
    PAYMENT_TYPES = [
        ('cash', '💵 Наличные'),
        ('card', '💳 Банковская карта'),
        ('apple_pay', ' Apple Pay'),
        ('google_pay', '📱 Google Pay'),
        ('sberbank', '🐷 Сбербанк Онлайн'),
        ('tinkoff', '💙 Тинькофф'),
        ('yoomoney', '💰 ЮMoney'),
        ('sbp', '🏦 СБП (Система быстрых платежей)'),
        ('corporate', '🏢 Корпоративный счет'),
    ]
    
    name = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES,
        verbose_name="Тип оплаты"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    icon = models.CharField(max_length=20, verbose_name="Иконка")
    description = models.TextField(blank=True, verbose_name="Описание")
    commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Комиссия (%)"
    )
    min_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name="Минимальная сумма"
    )
    max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100000.0,
        verbose_name="Максимальная сумма"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    def __str__(self):
        return self.get_name_display()
    
    def get_icon(self):
        """Возвращает иконку для типа оплаты"""
        icons = {
            'cash': '💵',
            'card': '💳',
            'apple_pay': '',
            'google_pay': '📱',
            'sberbank': '🐷',
            'tinkoff': '💙',
            'yoomoney': '💰',
            'sbp': '🏦',
            'corporate': '🏢',
        }
        return icons.get(self.name, '💳')
    
    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"
        ordering = ['order', 'name']


class Order(models.Model):
    """Модель заказа такси"""
    STATUS_CHOICES = [
        ('pending', '⏳ Ожидание'),
        ('accepted', '✅ Принят'),
        ('in_progress', '🚗 В пути'),
        ('completed', '🏁 Завершен'),
        ('cancelled', '❌ Отменен'),
    ]
    
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    pickup_address = models.TextField(verbose_name="Адрес подачи")
    destination_address = models.TextField(verbose_name="Адрес назначения")
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name="Тариф")
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Водитель")
    
    distance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Расстояние (км)")
    estimated_time = models.IntegerField(default=0, verbose_name="Примерное время (мин)")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая цена (₽)")
    
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Способ оплаты",
        related_name='payment_orders'  # ← ДОБАВЛЕНО: уникальное имя для обратной связи
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата оплаты"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.customer_name}"
    
    def calculate_price(self):
        """Расчет стоимости поездки"""
        base = self.tariff.base_price
        distance_price = self.distance * self.tariff.price_per_km
        time_price = (self.estimated_time / 60) * self.tariff.price_per_minute
        self.total_price = base + distance_price + time_price
        return self.total_price
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']


# Автоматическое создание способов оплаты после миграции
@receiver(post_migrate)
def create_default_payment_methods(sender, **kwargs):
    if sender.name == 'B0J_app':
        PaymentMethod.objects.get_or_create(
            name='cash',
            defaults={
                'icon': '💵',
                'description': 'Оплата наличными водителю при посадке или по прибытии',
                'commission': 0.0,
                'min_amount': 0.0,
                'max_amount': 10000.0,
                'order': 1
            }
        )
        
        PaymentMethod.objects.get_or_create(
            name='card',
            defaults={
                'icon': '💳',
                'description': 'Оплата банковской картой через терминал в автомобиле',
                'commission': 0.0,
                'min_amount': 0.0,
                'max_amount': 100000.0,
                'order': 2
            }
        )
        
        PaymentMethod.objects.get_or_create(
            name='apple_pay',
            defaults={
                'icon': '',
                'description': 'Бесконтактная оплата через Apple Pay',
                'commission': 0.0,
                'min_amount': 0.0,
                'max_amount': 100000.0,
                'order': 3
            }
        )
        
        PaymentMethod.objects.get_or_create(
            name='google_pay',
            defaults={
                'icon': '📱',
                'description': 'Бесконтактная оплата через Google Pay',
                'commission': 0.0,
                'min_amount': 0.0,
                'max_amount': 100000.0,
                'order': 4
            }
        )
        
        PaymentMethod.objects.get_or_create(
            name='sbp',
            defaults={
                'icon': '🏦',
                'description': 'Оплата через Систему быстрых платежей по QR-коду',
                'commission': 0.0,
                'min_amount': 0.0,
                'max_amount': 100000.0,
                'order': 5
            }
        )