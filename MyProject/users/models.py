from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from shop.models import Product


class Basket(models.Model):
    handler = models.ForeignKey('CustomUser', on_delete=models.CASCADE)


class CustomUser(AbstractUser, BaseUserManager):
    """Кастомная модель юзера, с телефоном и корзиной"""
    phone = models.CharField('User phone number', max_length=16, validators=[RegexValidator(r"^\+?\d{9,15}$")])


class CartItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='baskets')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=0)

