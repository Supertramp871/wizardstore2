from django.shortcuts import render, redirect  # Импорт функций для рендера шаблонов и перенаправления
from django.contrib import auth, messages  # Импорт для работы с аутентификацией и флеш-сообщениями
from django.urls import reverse  # Функция для построения URL по имени маршрута
from django.http import HttpResponseRedirect  # Для выполнения перенаправлений
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm  # Импорт форм приложения
from django.contrib.auth.decorators import login_required  # Декоратор для ограничения доступа к представлениям
from django.db.models import Prefetch  # Для оптимизации запросов с предвыборкой связанных объектов
from orders.models import Order, OrderItem  # Импорт моделей заказов и их элементов

# Представление для входа пользователя
def login(request):
    """
    Обрабатывает вход пользователя в систему.
    Если метод POST, проверяет форму, аутентифицирует и выполняет вход.
    Если метод GET, отображает форму входа.
    """
    if request.method == 'POST':  # Проверяет, что форма была отправлена
        form = UserLoginForm(data=request.POST)  # Создает форму с данными из запроса
        if form.is_valid():  # Проверяет, что данные формы корректны
            username = request.POST['username']  # Извлекает имя пользователя из данных формы
            password = request.POST['password']  # Извлекает пароль из данных формы
            user = auth.authenticate(username=username, password=password)  # Аутентификация пользователя
            if user:  # Если пользователь существует и данные корректны
                auth.login(request, user)  # Выполняет вход
                return HttpResponseRedirect(reverse('main:product_list'))  # Перенаправляет на список продуктов
    else:
        form = UserLoginForm()  # Пустая форма для отображения при GET-запросе
    return render(request, 'users/login.html', {'form': form})  # Рендер шаблона с формой

# Представление для регистрации нового пользователя
def registration(request):
    """
    Обрабатывает регистрацию нового пользователя.
    Если метод POST, сохраняет данные и выполняет вход.
    Если метод GET, отображает форму регистрации.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)  # Создает форму с данными из запроса
        if form.is_valid():  # Проверяет, что данные формы корректны
            form.save()  # Сохраняет нового пользователя
            user = form.instance  # Получает созданный экземпляр пользователя
            auth.login(request, user)  # Выполняет вход
            messages.success(request, f'{user.username}, Successful Registration')  # Добавляет сообщение об успехе
            return HttpResponseRedirect(reverse('user:login'))  # Перенаправляет на страницу входа
    else:
        form = UserRegistrationForm()  # Пустая форма для отображения при GET-запросе
    return render(request, 'users/registration.html', {'form': form})  # Рендер шаблона с формой

# Представление профиля пользователя
@login_required
def profile(request):
    """
    Отображает и обрабатывает изменения в профиле пользователя.
    Показывает также список заказов пользователя.
    """
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)  # Форма с текущими данными пользователя
        if form.is_valid():  # Проверяет, что данные формы корректны
            form.save()  # Сохраняет изменения профиля
            messages.success(request, 'Profile was changed')  # Добавляет сообщение об успехе
            return HttpResponseRedirect(reverse('user:profile'))  # Перенаправляет на страницу профиля
    else:
        form = ProfileForm(instance=request.user)  # Предзаполненная форма для отображения при GET-запросе
    
    # Получение заказов пользователя с предвыборкой товаров
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',  # Поле для предвыборки
            queryset=OrderItem.objects.select_related('product'),  # Запрос для получения связанных товаров
        )
    ).order_by('-id')  # Сортировка заказов по убыванию ID
    return render(request, 'users/profile.html',  # Рендер шаблона профиля
                  {'form': form, 'orders': orders})

# Представление для выхода пользователя
def logout(request):
    """
    Выполняет выход пользователя из системы и перенаправляет на главную страницу.
    """
    auth.logout(request)  # Выполняет выход
    return redirect(reverse('main:product_list'))  # Перенаправляет на список продуктов
