from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Basket, CartItem, CustomUser, UserReview


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'phone']


class BasketAdmin(admin.ModelAdmin):
    list_display = ['handler',]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['basket', 'product', 'quantity']

class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rate', 'pub_date']


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserReview, UserReviewAdmin)
