"""
ASGI config for wizardstore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os  # Импорт модуля для работы с системными переменными и путями
from django.core.asgi import get_asgi_application  # Импорт функции для создания ASGI приложения

# Устанавливаем переменную окружения, указывающую на модуль настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wizardstore.settings")

# Создаем экземпляр ASGI приложения, который будет использоваться сервером для обработки запросов
application = get_asgi_application()
