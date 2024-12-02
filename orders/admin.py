from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

# Встраиваем модель OrderItem в интерфейс администратора для отображения вместе с заказом
class OrderItemInline(admin.TabularInline):
    model = OrderItem  # Указываем модель, которую будем отображать в виде табличной строки
    raw_id_fields = ['product']  # Поле product будет отображаться как raw_id (упрощенный выбор)

# Функция для отображения ссылки на оплату через Stripe в админке
def order_stripe_payment(obj):
    url = obj.get_stripe_url()  # Получаем URL для Stripe платежа через метод модели
    if obj.stripe_id:  # Если есть stripe_id, то отображаем его в виде ссылки
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)  # mark_safe позволяет использовать HTML-код в выводе
    return ''  # Если нет stripe_id, возвращаем пустую строку

# Назначаем описание для колонки Stripe payment в админке
order_stripe_payment.short_description = 'Stripe payment'

# Регистрация модели Order в админке с дополнительными параметрами
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Определяем, какие поля будут отображаться в списке заказов
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_stripe_payment, 'created', 'updated']
    # Фильтры для отображения заказов по статусу оплаты и дате
    list_filter = ['paid', 'created', 'updated']
    # Встраиваем отображение заказанных товаров (OrderItem) в интерфейсе
    inlines = [OrderItemInline]
