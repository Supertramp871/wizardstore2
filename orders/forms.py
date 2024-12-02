from django import forms
from .models import Order

# Форма для создания заказа, основанная на модели Order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order  # Указываем модель, с которой работает форма
        fields = ['user', 'first_name', 'last_name', 'email',  # Перечисляем поля формы
                  'address', 'postal_code', 'city']

    # Конструктор формы с дополнительной логикой для автозаполнения полей
    def __init__(self, *args, **kwargs):
        # Извлекаем объект request из аргументов
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Если пользователь аутентифицирован, заполняем поля формы из данных пользователя
        if self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email
    
    # Метод сохранения формы, с учетом текущего пользователя
    def save(self, commit=True):
        order = super().save(commit=False)  # Создаем объект заказа без сохранения в БД
        if self.request.user.is_authenticated:  # Если пользователь аутентифицирован, сохраняем его
            order.user = self.request.user
        else:
            order.user = None  # Если пользователь не аутентифицирован, связываем заказ с None
        if commit:  # Если commit=True, сохраняем заказ в БД
            order.save()
        return order  # Возвращаем объект заказа
