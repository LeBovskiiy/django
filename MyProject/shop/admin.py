from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import Product, ProductCategory, ProductTags


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    """Продукты"""
    description_ru = forms.CharField(label='Описание')
    description_en = forms.CharField(label='Description')
    list_display = ('name', 'price',)
    list_display_links = ('name',)
    

@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    """Категории"""
    # category_ru = forms.CharField(label='Категория')
    # category_en = forms.CharField(label='Category')
    list_display = ('category',)
    

@admin.register(ProductTags)
class ProductTagsAdmin(TranslationAdmin):
    """Теги"""
    list_display = ('tag_name',)

