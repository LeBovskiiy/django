from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from shop.models import Product

class UserBasket(models.Model):
    basket = models.ManyToManyField(Product, related_name='basket_p', auto_created=True, default=None)
    handler = models.OneToOneField('CustomUser', on_delete=models.CASCADE)


class CustomUser(AbstractUser, BaseUserManager):
    """Кастомная модель юзера, с телефоном и корзиной"""
    phone = models.CharField('User phone number', max_length=16, validators=[RegexValidator(r"^\+?\d{9,15}$")])

