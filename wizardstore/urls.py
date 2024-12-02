"""
URL configuration for wizardstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # Импорт административной панели
from django.urls import path, include  # Импорт функций для определения URL-маршрутов
from django.conf import settings  # Импорт настроек проекта
from django.conf.urls.static import static  # Для работы со статическими и медиа-файлами

# Основной список маршрутов (urlpatterns)
urlpatterns = [
    path("admin/", admin.site.urls),  # URL для административной панели
    path("cart/", include('cart.urls', namespace='cart')),  # Подключение маршрутов приложения "cart"
    path("user/", include('users.urls', namespace='user')),  # Подключение маршрутов приложения "users"
    path('orders/', include('orders.urls', namespace='orders')),  # Подключение маршрутов приложения "orders"
    path('payment/', include('payment.urls', namespace='payment')),  # Подключение маршрутов приложения "payment"
    path('', include('main.urls', namespace='main')),  # Основная страница приложения "main"
]

# Дополнение маршрутов для обработки медиа-файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # MEDIA_URL — URL для медиа-файлов
    # MEDIA_ROOT — путь к директории, где хранятся медиа-файлы
