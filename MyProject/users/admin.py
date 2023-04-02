from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Basket, CartItem


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'phone']


class BasketAdmin(admin.ModelAdmin):
    list_display = ['handler',]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['basket', 'product', 'quantity']


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(CustomUser, CustomUserAdmin)