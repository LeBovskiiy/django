from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from shop.models import Product


class CustomUser(AbstractUser, BaseUserManager):
    """Кастомная аутентификацыя"""
    phone = models.CharField('User phone number', max_length=16, validators=[RegexValidator(r"^\+?\d{9,15}$")])


class UserBasket(models.Model):
    """Корзина для пользователя, где будут храниться товары"""
    handler = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    basket = models.ForeignKey(to=Product, on_delete=models.CASCADE, blank=True, null=True)
