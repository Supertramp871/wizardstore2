from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem  # Импорт модели OrderItem для создания элементов заказа
from .forms import OrderCreateForm  # Импорт формы для создания заказа
from cart.cart import Cart  # Импорт класса Cart для работы с корзиной

# Представление для создания нового заказа
def order_create(request):
    cart = Cart(request)  # Получаем объект корзины, связанный с текущим запросом
    if request.method == 'POST':  # Если метод запроса POST (когда отправляется форма)
        form = OrderCreateForm(request.POST, request=request)  # Создаем форму для создания заказа с данными из POST-запроса
        if form.is_valid():  # Если форма валидна
            order = form.save()  # Сохраняем заказ в базе данных
            # Для каждого товара в корзине создаем элемент заказа
            for item in cart:
                discounted_price = item['product'].sell_price()  # Вычисляем цену с учетом скидки
                # Создаем новый объект OrderItem для каждого товара в корзине
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # Очищаем корзину после создания заказа
            request.session['order_id'] = order.id  # Сохраняем ID заказа в сессии, чтобы передать его в процесс оплаты
            return redirect(reverse('payment:process'))  # Перенаправляем на процесс оплаты
    else:  # Если метод запроса GET (отображение формы)
        form = OrderCreateForm(request=request)  # Создаем пустую форму для заказа
    # Отображаем шаблон с корзиной и формой для создания заказа
    return render(request, 
                  'orders/order/create.html',  # Путь к шаблону
                  {'cart': cart,  # Передаем корзину в шаблон
                   'form': form})  # Передаем форму для создания заказа в шаблон
