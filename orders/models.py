from django.db import models
from main.models import Product  # Импорт модели Product из приложения main
from users.models import User  # Импорт модели User из приложения users
from django.conf import settings  # Импорт настроек Django

# Модель для заказа
class Order(models.Model):
    # Связь с пользователем, если он есть
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True, null=True, default=None)
    # Поля для данных заказа
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)  # Время создания заказа
    updated = models.DateTimeField(auto_now=True)  # Время последнего обновления
    paid = models.BooleanField(default=False)  # Статус оплаты
    stripe_id = models.CharField(max_length=250, blank=True)  # ID для Stripe, если применимо

    # Метаданные модели
    class Meta:
        ordering = ['-created']  # Заказы сортируются по дате создания в убывающем порядке
        indexes = [
            models.Index(fields=['-created']),  # Индекс по полю created для быстрого поиска
        ]
        
    # Строковое представление заказа
    def __str__(self):
        return f'Order {self.id}'
    
    # Метод для вычисления общей стоимости заказа
    def get_total_cost(self):
        # Суммируем стоимость всех товаров в заказе
        return sum(item.get_cost() for item in self.items.all())
    
    # Метод для получения ссылки на платеж в Stripe
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''  # Если нет stripe_id, возвращаем пустую строку
        # Если в ключе секретного API Stripe используется "_test_", добавляем путь '/test/'
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        # Формируем и возвращаем ссылку на платеж в Stripe
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

# Модель для элементов заказа (каждого товара в заказе)
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',  # Связь с заказом
                              on_delete=models.CASCADE)  # Удаляем элементы, если заказ удаляется
    product = models.ForeignKey(Product,
                                related_name='order_items',  # Связь с продуктом
                                on_delete=models.CASCADE)  # Удаляем элементы, если продукт удаляется
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    quantity = models.PositiveIntegerField(default=1)  # Количество товара в заказе

    # Строковое представление элемента заказа
    def __str__(self):
        return str(self.id)
    
    # Метод для вычисления стоимости этого элемента заказа
    def get_cost(self):
        return self.price * self.quantity  # Стоимость = цена * количество
