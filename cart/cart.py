from decimal import Decimal  # Импорт для работы с точными десятичными числами
from django.conf import settings  # Для получения настроек из конфигурации Django
from main.models import Product  # Импорт модели Product для работы с продуктами

class Cart:
    """
    Класс для работы с корзиной покупок.
    Хранит корзину в сессии пользователя.
    """

    def __init__(self, request):
        """
        Инициализация корзины из сессии пользователя.
        Если корзина не существует, создается новая.
        """
        self.session = request.session  # Доступ к сессии текущего пользователя
        cart = self.session.get(settings.CART_SESSION_ID)  # Получение корзины из сессии
        if not cart:  # Если корзина не существует
            cart = self.session[settings.CART_SESSION_ID] = {}  # Создание новой корзины в сессии
        self.cart = cart  # Сохранение корзины в атрибут класса

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавление товара в корзину.
        Если товар уже в корзине, обновляет его количество.
        Если параметр override_quantity = True, заменяет количество товара.
        """
        product_id = str(product.id)  # Преобразуем id товара в строку для использования в сессии
        if product_id not in self.cart:  # Если товара еще нет в корзине
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}  # Добавляем товар с нулевым количеством и ценой
        if override_quantity:  # Если нужно переопределить количество
            self.cart[product_id]['quantity'] = quantity  # Устанавливаем новое количество
        else:
            self.cart[product_id]['quantity'] += quantity  # Увеличиваем количество товара
        self.save()  # Сохраняем изменения в сессии

    def save(self):
        """
        Помечает сессию как измененную, чтобы изменения сохранялись.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Удаляет товар из корзины.
        """
        product_id = str(product.id)  # Преобразуем id товара в строку
        if product_id in self.cart:  # Если товар есть в корзине
            del self.cart[product_id]  # Удаляем его из корзины
            self.save()  # Сохраняем изменения в сессии

    def __iter__(self):
        """
        Позволяет перебирать товары в корзине.
        Загружает информацию о товарах из базы данных и добавляет их в корзину.
        """
        product_ids = self.cart.keys()  # Получаем список id товаров в корзине
        products = Product.objects.filter(id__in=product_ids)  # Загружаем товары из базы данных
        cart = self.cart.copy()  # Копируем корзину, чтобы не изменять оригинал
        for product in products:  # Для каждого товара в корзине
            cart[str(product.id)]['product'] = product  # Добавляем информацию о товаре
        for item in cart.values():  # Перебираем все элементы в корзине
            item['price'] = Decimal(item['price'])  # Преобразуем цену в десятичный формат для точных расчетов
            item['total_price'] = item['price'] * item['quantity']  # Рассчитываем полную стоимость товара
            yield item  # Возвращаем товар с его ценой и общей стоимостью

    def __len__(self):
        """
        Возвращает общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())  # Суммируем количество всех товаров

    def clear(self):
        """
        Очищает корзину в сессии пользователя.
        """
        del self.session[settings.CART_SESSION_ID]  # Удаляет корзину из сессии

    def get_total_price(self):
        """
        Возвращает общую стоимость товаров в корзине с учетом скидок.
        """
        total = sum(
            (Decimal(item['price']) - (Decimal(item['price'])  # Применяем скидку
            * Decimal(item['product'].discount / 100))) * item['quantity']
            for item in self.cart.values())  # Для каждого товара рассчитываем стоимость с учетом количества
        return format(total, '.2f')  # Форматируем итоговую стоимость с двумя знаками после запятой
