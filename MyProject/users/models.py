from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import get_object_or_404

from shop.models import Product

class BasketManager(models.Manager):
    
    def get_handler(self, user):
        return Basket.objects.get(handler=user)
        

class Basket(models.Model):
    handler = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE,
        related_name='handlers'
        )
    objects = BasketManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return self.handler.username
    

class CustomUser(AbstractUser, BaseUserManager):
    """Кастомная модель юзера, с телефоном и корзиной"""
    phone = models.CharField(
        'User phone number', 
        max_length=16,
        validators=[RegexValidator(
        r"^\+?\d{9,15}$")]
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class CartItemManager(models.Manager):
    
    def get_cart_items(self, basket: Basket):
        return basket.baskets.all()
    
    def add_quantity(self, product_id, user: 'request.user'):
        product = get_object_or_404(Product, id=product_id)
        basket, created = Basket.objects.get_or_create(handler=user)
        cart_items, created = CartItem.objects.get_or_create(
            basket=basket, 
            product=product
            )
        if cart_items:
            cart_items.quantity += 1
            cart_items.save()
        else:
            return False
        return True
            
    def subtract_quantity(self, product_id, user):
        product = get_object_or_404(Product, id=product_id)
        basket, created = Basket.objects.get_or_create(handler=user)
        cart_items, created = CartItem.objects.get_or_create(
            basket=basket, 
            product=product
            )
        if cart_items:
            if cart_items.quantity >= 1:
                cart_items.quantity -= 1
                cart_items.save()
            else:
                cart_items.delete()
        else:
            return False
        return True
                
    def delete_cart_item(self, product_id, user):
        product = get_object_or_404(Product, id=product_id)
        basket, created = Basket.objects.get_or_create(handler=user)
        cart_items, created = CartItem.objects.get_or_create(
            basket=basket, 
            product=product
            )
        if cart_items:
            cart_items.delete()
        else:
            return False
        return True
    
    def get_items(self, user):
        items = CartItem.objects.filter(
            basket=Basket.objects
            .get(handler=user)) \
            .select_related('product')
        return items


class CartItem(models.Model):
    basket = models.ForeignKey(
        Basket, 
        on_delete=models.CASCADE, 
        related_name='baskets'
        )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='products'
        )
    quantity = models.PositiveIntegerField(
        default=0
        )
    objects = CartItemManager()

    class Meta:
        verbose_name = 'Карта с продуктами'
        verbose_name_plural = 'Карты с продуктами'

    def __str__(self) -> str:
        return self.basket.handler.username


class UserRate(models.IntegerChoices):
    BAD = 1, 'Very Bad'
    NOT_GOOD = 2, 'Not Good'
    MIDDLE = 3, 'Middle'
    GOOD = 4, 'Good'
    VERY_GOOD = 5, 'Very Good'


class UserReview(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.PROTECT,
        related_name='users'
        )
    comment = models.TextField(
        verbose_name='Коментарий пользователя', 
        blank=True, null=True
        )
    rate = models.IntegerField(
        choices=UserRate.choices)
    product = models.ForeignKey(
        to=Product, 
        on_delete=models.DO_NOTHING, 
        related_name='comments'
        )
    pub_date = models.DateField(
        auto_now_add=True
        )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self) -> str:
        return str(self.user)
    