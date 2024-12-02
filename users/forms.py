from django import forms  # Импортирует стандартные классы форм Django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm  
# Импортирует встроенные формы для аутентификации, регистрации и изменения данных пользователя
from .models import User  # Импорт кастомной модели пользователя

# Форма для входа пользователя
class UserLoginForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя.
    """
    username = forms.CharField()  # Поле ввода имени пользователя
    password = forms.CharField()  # Поле ввода пароля

    class Meta:
        model = User  # Указывает, что форма работает с кастомной моделью User
        fields = ['username', 'password']  # Поля, которые используются в форме

# Форма для регистрации нового пользователя
class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.
    """
    class Meta:
        model = User  # Указывает, что форма работает с кастомной моделью User
        fields = (
            'first_name',  # Имя пользователя
            'last_name',   # Фамилия пользователя
            'username',    # Имя пользователя для входа
            'email',       # Email пользователя
            'password1',   # Пароль
            'password2',   # Подтверждение пароля
        )

    # Дополнительные настройки полей (необязательно, так как Meta уже задает поля)
    first_name = forms.CharField()  
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

# Форма для изменения профиля пользователя
class ProfileForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User  # Указывает, что форма работает с кастомной моделью User
        fields = (
            'image',       # Аватар пользователя
            'first_name',  # Имя пользователя
            'last_name',   # Фамилия пользователя
            'username',    # Имя пользователя для входа
            'email',       # Email пользователя
        )

    # Поля формы с дополнительными настройками (если требуется)
    image = forms.ImageField(required=False)  # Поле для загрузки аватара, не обязательно
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
