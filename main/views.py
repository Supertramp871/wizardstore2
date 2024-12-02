from django.shortcuts import render, get_object_or_404  # Функции для рендеринга и получения объектов или возврата 404
from .models import Product, Category  # Импорт моделей продуктов и категорий
from django.core.paginator import Paginator  # Класс для разбиения объектов на страницы
from cart.forms import CartAddProductForm  # Форма для добавления товаров в корзину

# Отображение популярных продуктов
def popular_list(request):
    """
    Отображает список из трех популярных продуктов на главной странице.
    """
    products = Product.objects.filter(available=True)[:3]  
    # Получает три доступных продукта
    return render(request, 'main/index/index.html', {'products': products})  
    # Рендерит шаблон с продуктами

# Детальная страница продукта
def product_detail(request, slug):
    """
    Отображает детальную информацию о продукте.
    """
    product = get_object_or_404(Product, slug=slug, available=True)  
    # Получает продукт по slug или возвращает 404, если продукт недоступен
    cart_product_form = CartAddProductForm  
    # Форма для добавления товара в корзину
    return render(
        request, 
        'main/product/detail.html', 
        {'product': product, 'cart_product_form': cart_product_form}
    )  
    # Рендерит шаблон с продуктом и формой

# Список продуктов с фильтрацией и пагинацией
def product_list(request, category_slug=None):
    """
    Отображает список продуктов с возможностью фильтрации по категории и пагинацией.
    """
    page = request.GET.get('page', 1)  
    # Получает текущую страницу из запроса, по умолчанию 1
    category = None  
    # Текущая категория (если указана)
    categories = Category.objects.all()  
    # Получает все категории
    products = Product.objects.filter(available=True)  
    # Получает доступные продукты

    paginator = Paginator(products, 10)  
    # Создает пагинатор для разбиения продуктов по 10 на страницу
    current_page = paginator.page(int(page))  
    # Получает текущую страницу из пагинатора

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)  
        # Получает категорию по slug или возвращает 404
        paginator = Paginator(products.filter(category=category), 10)  
        # Создает пагинатор для продуктов выбранной категории
        current_page = paginator.page(int(page))  
        # Получает текущую страницу для отфильтрованных продуктов

    return render(
        request, 
        'main/product/list.html', 
        {
            'category': category,  # Текущая категория
            'categories': categories,  # Список всех категорий
            'products': current_page,  # Продукты на текущей странице
            'slug_url': category_slug,  # URL текущей категории
        }
    )  
    # Рендерит шаблон со списком продуктов
