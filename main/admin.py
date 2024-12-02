from django.contrib import admin  # Импорт модуля для настройки административной панели
from .models import Product, Category  # Импорт моделей Product и Category из текущего приложения

# Регистрация моделей для административной панели

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Category в административной панели.
    """
    list_display = ['name', 'slug']  # Поля, отображаемые в списке категорий
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение поля 'slug' на основе значения поля 'name'


@admin.register(Product)
class ProducAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Product в административной панели.
    """
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'discount']  
    # Поля, отображаемые в списке товаров

    list_filter = ['available', 'created', 'updated']  
    # Фильтры для быстрого поиска товаров по доступности и дате создания/обновления

    list_editable = ['price', 'available', 'discount']  
    # Поля, которые можно редактировать прямо из списка товаров

    prepopulated_fields = {'slug': ('name',)}  
    # Автозаполнение поля 'slug' на основе значения поля 'name'
