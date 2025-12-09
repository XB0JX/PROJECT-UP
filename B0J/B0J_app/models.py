from django.db import models

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