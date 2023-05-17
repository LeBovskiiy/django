from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from shop.models import Product


class Basket(models.Model):
    handler = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.handler.username + 'basket'


class CustomUser(AbstractUser, BaseUserManager):
    """Кастомная модель юзера, с телефоном и корзиной"""
    phone = models.CharField('User phone number', max_length=16, validators=[RegexValidator(r"^\+?\d{9,15}$")])


class CartItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='baskets')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=0)


class UserRate(models.IntegerChoices):
    BAD = 1, 'Very Bad'
    NOT_GOOD = 2, 'Not Good'
    MIDDLE = 3, 'Middle'
    GOOD = 4, 'Good'
    VERY_GOOD = 5, 'Very Good'


class UserReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name='Коментарий пользователя', blank=True, null=True)
    rate = models.IntegerField(choices=UserRate.choices)
    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name='comments')
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)
