from django.db import models


def user_directory_path(instance, filename):
    '''Этот метод создан для генерациы имени файла'''
    return f'shop/{instance.name}_{filename}'

class ProductManager(models.Manager):
    
    def on_home(self):
        return Product.objects.all()
    
    def filter_by_name(self, product_name: str):
        return Product.objects.filter(name__istartswith=product_name)

    def get_commets(self, product_id):
        return Product.objects.get(id=product_id).comments.all()


class Product(models.Model):
    '''Модель продукта'''
    name = models.CharField(
        max_length=200, 
        verbose_name='Product name'
        )
    description = models.TextField(
        max_length=500, 
        verbose_name='Product discription'
        )
    price = models.IntegerField(verbose_name='Price')
    image = models.ImageField(
        upload_to=user_directory_path, 
        verbose_name='Photo', 
        blank=True, 
        null=True
        )
    tags = models.ManyToManyField(
        to='ProductTags', 
        blank=True,
        related_name='product_tags'
        )
    categories = models.ManyToManyField(
        to='ProductCategory', 
        blank=True, 
        related_name='product_category'
        )
    quantity = models.PositiveIntegerField(default=1)
    objects = ProductManager()
    comment = ProductManager()
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    '''Теги продукта'''
    tag_name = models.CharField(
        max_length=30, 
        verbose_name='Product tags'
        )

    class Meta:
        verbose_name = 'Тег продукта'
        verbose_name_plural = 'Теги продуктов'

    def __str__(self):
        return self.tag_name


class ProductCategoryManager(models.Manager):
        
    def get_all_categories(self):
        return ProductCategory.objects.all()
    
    def get_products_by_category(self, category_name):
        return ProductCategory.objects \
            .get(category=category_name) \
            .product_category.all()
    
    
class ProductCategory(models.Model):
    '''Категория продукта'''
    category = models.CharField(
        max_length=30, 
        verbose_name='Product category'
        )
    objects = ProductCategoryManager()
    
    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.category
