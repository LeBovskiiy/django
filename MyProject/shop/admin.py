from django.contrib import admin

from .models import Product, ProductTags, ProductCategory

admin.site.register(Product)
admin.site.register(ProductTags)
admin.site.register(ProductCategory)

