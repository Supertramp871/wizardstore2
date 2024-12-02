from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from orders.models import Order  # Импорт модели Order для получения данных заказа
from django.conf import settings  # Импорт настроек для Stripe
import stripe  # Импорт библиотеки Stripe для работы с платежами

# Устанавливаем ключ API для работы с Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY  # Ключ для доступа к Stripe API
stripe.api_version = settings.STRIPE_API_VERSION  # Указание версии API

# Представление для обработки платежа
def payment_process(request):
    order_id = request.session.get('order_id', None)  # Получаем ID заказа из сессии
    order = get_object_or_404(Order, id=order_id)  # Ищем заказ по ID, если не найден - возвращаем ошибку 404
    
    if request.method == 'POST':  # Если метод запроса POST (когда отправляется форма)
        # Формируем URL для успешного завершения и отмены платежа
        success_url = request.build_absolute_uri(
            reverse('payment:completed')  # URL успешного завершения
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')  # URL отмены платежа
        )
        
        # Формируем данные для сессии Stripe Checkout
        session_data = {
            'mode': 'payment',  # Режим - платеж
            'client_reference_id': order.id,  # ID заказа
            'success_url': success_url,  # URL для успешной оплаты
            'cancel_url': cancel_url,  # URL для отмены оплаты
            'line_items': []  # Список товаров, которые будут отображаться в Stripe Checkout
        }

        # Добавляем товары из заказа в line_items
        for item in order.items.all():  # Для каждого товара в заказе
            discounted_price = item.product.sell_price()  # Получаем цену товара с учетом скидки
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(discounted_price * Decimal('100')),  # Цена в центах
                    'currency': 'usd',  # Валюта
                    'product_data': {
                        'name': item.product.name,  # Название товара
                    },
                },
                'quantity': item.quantity,  # Количество товара
            })
        
        # Создаем сессию платежа в Stripe
        session = stripe.checkout.Session.create(**session_data)
        
        # Перенаправляем на URL Stripe Checkout
        return redirect(session.url, code=303)
    else:  # Если метод запроса GET (отображение страницы)
        return render(request, 'payment/process.html', locals())  # Отображаем страницу с формой для платежа


# Представление для успешного завершения платежа
def payment_completed(request):
    return render(request, 'payment/completed.html')  # Отображаем страницу успешной оплаты


# Представление для отмены платежа
def payment_canceled(request):
    return render(request, 'payment/canceled.html')  # Отображаем страницу отмены оплаты
