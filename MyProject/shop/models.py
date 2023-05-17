from django.db import models


def user_directory_path(instance, filename):
    """Этот метод создан для генерациы имени файла"""
    return f'shop/{instance.name}_{filename}'


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=200, verbose_name="Product name")
    description = models.TextField(max_length=500, verbose_name="Product discription")
    price = models.IntegerField(verbose_name="Price")
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Photo', blank=True, null=True)
    tags = models.ManyToManyField(to="ProductTags", blank=True)
    categories = models.ManyToManyField(to="ProductCategory", blank=True, related_name='product_category')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    """Теги продукта"""
    tag_name = models.CharField(max_length=30, verbose_name='Product tags')

    def __str__(self):
        return self.tag_name


class ProductCategory(models.Model):
    """Категория продукта"""
    category = models.CharField(max_length=30, verbose_name='Product category')

    def __str__(self):
        return self.category
