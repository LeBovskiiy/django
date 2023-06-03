from shop.models import Product, ProductCategory
from django.core.files.uploadedfile import SimpleUploadedFile

import random

def category_range() ->  int or None:
    ran = random.randint(1, 100)
    ran1 = random.randint(1, 100)
    ran2 = random.randint(1, 100)
    return (ran, ran1, ran2)

def create_tables():
    file_content = b'test_file'
    file_name = 'product_name_test_file.png'
    file = SimpleUploadedFile(file_name, file_content, content_type='image/png')
    
    for i in range(100):
        ProductCategory.objects.create(
            category=f'category{i}'
        )
    
    for i in range(1000):
        product = Product.objects.create(
            name=f'product{i}',
            description=f'description for product number: {i}',
            price=random.randint(1, 5000),
            image=file
            
        )
        cate_range, cate_range1, cate_range2 = category_range()
        product.categories.set([cate_range, cate_range1, cate_range2])
    