from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Basket, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_basket(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(handler=instance)


