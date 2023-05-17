from django.contrib import admin

from .models import Product, ProductCategory, ProductTags

admin.site.register(Product)
admin.site.register(ProductTags)
admin.site.register(ProductCategory)

