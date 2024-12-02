import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order  # Импорт модели Order для обновления состояния заказа
from main.models import Product  # Импорт модели Product, хотя она не используется в этом файле

# Отключаем проверку CSRF, так как Stripe будет отправлять запросы напрямую
@csrf_exempt
def stripe_webhook(request):
    payload = request.body  # Получаем тело запроса (данные, отправленные Stripe)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']  # Получаем заголовок подписи для проверки
    event = None  # Инициализация переменной для события

    try:
        # Проверяем подлинность события с помощью ключа подписи и вебхука
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET  # Секретный ключ для верификации от Stripe
        )
    except ValueError as e:
        # Если произошла ошибка при обработке события, возвращаем 400
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Если не удается подтвердить подпись, возвращаем 400
        return HttpResponse(status=400)
    
    # Проверяем, что событие - успешная оплата
    if event.type == 'checkout.session.completed':
        session = event.data.object  # Получаем объект сессии из события
        if session.mode == 'payment' and session.payment_status == 'paid':  # Проверяем, что оплата прошла
            try:
                # Ищем заказ, ссылаясь на client_reference_id, который был передан в сессии
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                # Если заказ не найден, возвращаем 404
                return HttpResponse(status=404)
            
            # Обновляем статус оплаты заказа
            order.paid = True
            order.stripe_id = session.payment_intent  # Сохраняем stripe_id для будущих проверок
            order.save()  # Сохраняем изменения в заказе
    
    # Ответ от Stripe, чтобы подтвердить получение вебхука
    return HttpResponse(status=200)
