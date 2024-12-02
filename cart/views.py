from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Обработчик для добавления товара в корзину
@require_POST  # Указываем, что данный обработчик работает только для POST-запросов
def cart_add(request, product_id):
    cart = Cart(request)  # Инициализируем корзину для текущего запроса
    product = get_object_or_404(Product, id=product_id)  # Получаем товар по ID или 404, если не найден
    form = CartAddProductForm(request.POST)  # Создаем форму для добавления товара в корзину
    if form.is_valid():  # Проверяем, валидна ли форма
        cd = form.cleaned_data  # Получаем очищенные данные из формы
        # Добавляем товар в корзину с количеством и флагом переопределения количества
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')  # Перенаправляем на страницу с деталями корзины

# Обработчик для удаления товара из корзины
@require_POST  # Указываем, что данный обработчик работает только для POST-запросов
def cart_remove(request, product_id):
    cart = Cart(request)  # Инициализируем корзину для текущего запроса
    product = get_object_or_404(Product, id=product_id)  # Получаем товар по ID или 404, если не найден
    cart.remove(product)  # Удаляем товар из корзины
    return redirect('cart:cart_detail')  # Перенаправляем на страницу с деталями корзины

# Функция для отображения содержимого корзины
def cart_detail(request):
    cart = Cart(request)  # Инициализируем корзину для текущего запроса
    return render(request, 'cart/detail.html', {'cart': cart})  # Рендерим страницу с деталями корзины
