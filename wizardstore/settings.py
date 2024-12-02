"""
Django settings for wizardstore project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path  # Модуль для работы с путями файловой системы

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Быстрые настройки для разработки (не подходят для продакшена)
# Подробнее: https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Секретный ключ проекта, который используется для криптографических операций
# Этот ключ необходимо держать в секрете в продакшене
SECRET_KEY = ""

# Режим отладки (включен для разработки, выключен для продакшена)
DEBUG = True

# Список хостов, с которых сервер принимает запросы (в продакшене нужно указать реальные домены)
ALLOWED_HOSTS = []


# Определение установленных приложений
INSTALLED_APPS = [
    "django.contrib.admin",  # Административная панель
    "django.contrib.auth",  # Аутентификация и управление пользователями
    "django.contrib.contenttypes",  # Система для работы с типами контента
    "django.contrib.sessions",  # Управление пользовательскими сессиями
    "django.contrib.messages",  # Работа с сообщениями
    "django.contrib.staticfiles",  # Обработка статических файлов
    "main",  # Приложение для основной функциональности
    "cart",  # Приложение для корзины
    "users",  # Приложение для управления пользователями
    "orders",  # Приложение для заказов
    "payment",  # Приложение для обработки платежей
]

# Определение промежуточного ПО (middleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Безопасность (например, HTTPS)
    "django.contrib.sessions.middleware.SessionMiddleware",  # Управление сессиями
    "django.middleware.common.CommonMiddleware",  # Общие улучшения запросов и ответов
    "django.middleware.csrf.CsrfViewMiddleware",  # Защита от CSRF-атак
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Аутентификация пользователей
    "django.contrib.messages.middleware.MessageMiddleware",  # Работа с сообщениями
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Защита от clickjacking
]

# Основной URL-конфиг проекта
ROOT_URLCONF = "wizardstore.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Использование шаблонизатора Django
        "DIRS": [],  # Дополнительные директории для шаблонов
        "APP_DIRS": True,  # Автоматический поиск шаблонов в приложениях
        "OPTIONS": {
            "context_processors": [  # Контекстные процессоры для добавления переменных в шаблоны
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",  # Кастомный процессор для корзины
            ],
        },
    },
]

# Настройка WSGI-приложения
WSGI_APPLICATION = "wizardstore.wsgi.application"


# Настройки базы данных
# Подробнее: https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Используем PostgreSQL
        "NAME": "wizardstore",  # Имя базы данных
        "USER": "postgres",  # Имя пользователя
        "PASSWORD": "postgres",  # Пароль пользователя
        "HOST": "localhost",  # Хост базы данных
        "PORT": "5432",  # Порт базы данных
    }
}


# Валидаторы паролей
# Подробнее: https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Настройки интернационализации
# Подробнее: https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"  # Язык по умолчанию
TIME_ZONE = "UTC"  # Часовой пояс
USE_I18N = True  # Включение интернационализации
USE_TZ = True  # Включение поддержки временных зон


# Настройки статических файлов
# Подробнее: https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/"  # URL для доступа к статическим файлам

# Настройки загрузки медиа-файлов
MEDIA_URL = 'media/'  # URL для доступа к медиа-файлам
MEDIA_ROOT = BASE_DIR / 'media'  # Локальный путь для сохранения медиа-файлов

# Настройка корзины
CART_SESSION_ID = 'cart'  # ID для хранения данных корзины в сессии

# Кастомная модель пользователя
AUTH_USER_MODEL = 'users.User'  # Указание на кастомную модель User

# Настройки Stripe API
STRIPE_PUBLISHABLE_KEY = 'pk_test_51QK5LJBBrKRd4HNrtAWEmR3caZANGsPIitsosozPyZszDXuKf5w21OWGLRmQWd4UK0TyqZvwLf6EVtVBYxb0tkWr00idrNdVYM'
STRIPE_SECRET_KEY = 'sk_test_51QK5LJBBrKRd4HNr6qrCxHmsLM68jxs50Sh6zPbSgtMTZV7Ts2zQN9F4mmrwA6L5IzHvG83LzV8L12cZdImJeWqW00UQaFY57E'
STRIPE_API_VERSION = '2022-08-01'  # Версия API Stripe
STRIPE_WEBHOOK_SECRET = 'whsec_a0ecba97f973d6b4aae54f94c9a570c28174433d17713b8a016899e4fd9740a3'

# Настройка автосоздания полей
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Тип полей для автоматических первичных ключей
