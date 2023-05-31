from rest_framework import serializers

from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 
            'description', 
            'price', 
            'image', 
            'categories',
            )
        
        
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'category',
        )
        
        
class ProductByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 
            'description', 
            'price', 
            'image', 
            'categories',
        )