from django.db import models  # Импорт модуля для создания моделей
from django.urls import reverse  # Импорт функции для генерации URL

# Определение моделей приложения

class Category(models.Model):
    """
    Модель для категорий продуктов.
    """
    name = models.CharField(max_length=20, unique=True)  
    # Название категории, уникальное, с максимальной длиной 20 символов

    slug = models.SlugField(max_length=20, unique=True)  
    # Поле для URL-идентификатора категории, уникальное

    class Meta:
        """
        Метаданные модели.
        """
        ordering = ['name']  # Сортировка категорий по имени
        indexes = [models.Index(fields=['name'])]  # Индекс для ускорения поиска по имени
        verbose_name = 'category'  # Название модели в единственном числе
        verbose_name_plural = 'categories'  # Название модели во множественном числе

    def get_absolute_url(self):
        """
        Генерация абсолютного URL для категории.
        """
        return reverse("main:product_list_by_category", args=[self.slug])

    def __str__(self):
        """
        Строковое представление категории.
        """
        return self.name


class Product(models.Model):
    """
    Модель для продуктов.
    """
    category = models.ForeignKey(
        Category,
        related_name='products',  # Связь с категорией (один ко многим)
        on_delete=models.CASCADE  # При удалении категории удаляются связанные продукты
    )
    name = models.CharField(max_length=50)  # Название продукта
    slug = models.SlugField(max_length=50)  # URL-идентификатор продукта
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)  
    # Изображение продукта, сохраняемое в папке с шаблоном даты
    description = models.TextField(blank=True)  # Описание продукта
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    # Цена продукта, до 10 цифр с 2 знаками после запятой
    available = models.BooleanField(default=True)  
    # Доступность продукта (в продаже или нет)
    created = models.DateTimeField(auto_now_add=True)  
    # Дата создания продукта (устанавливается автоматически при создании)
    updated = models.DateTimeField(auto_now=True)  
    # Дата обновления продукта (автоматически обновляется при изменении записи)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)  
    # Скидка на продукт (в процентах)

    class Meta:
        """
        Метаданные модели.
        """
        ordering = ['name']  # Сортировка продуктов по имени
        indexes = [
            models.Index(fields=['id', 'slug']),  # Индекс для поиска по ID и URL
            models.Index(fields=['name']),  # Индекс для поиска по имени
            models.Index(fields=['-created']),  # Индекс для поиска по дате создания (в обратном порядке)
        ]

    def __str__(self):
        """
        Строковое представление продукта.
        """
        return self.name

    def get_absolute_url(self):
        """
        Генерация абсолютного URL для продукта.
        """
        return reverse('main:product_detail', args=[self.slug])

    def sell_price(self):
        """
        Вычисление цены продукта с учетом скидки.
        Если скидка указана, вычисляет цену со скидкой.
        """
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
