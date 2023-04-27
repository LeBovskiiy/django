from django.test import TestCase, Client

import os
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product, ProductCategory
from .views import *


class ProductTests(TestCase):

    def setUp(self):
        file_content = b'test_file'
        file_name = 'product_name_test_file.png'
        self.upload_file = SimpleUploadedFile(file_name, file_content, content_type='image/png')
        ProductCategory.objects.create(category='category name')
        category = ProductCategory.objects.get(id=1)
        Product.objects.create(name='product_name',  description='description', price=500, image=self.upload_file)
        c = Client()
        response = c.post('/login/', {"username": "John", "password": "123456789"})
        response.status_code

    def test_product(self):
        prododuct=Product.objects.get(id=1)
        category=ProductCategory.objects.get(id=1)
        self.assertEqual(prododuct.name, 'product_name')
        self.assertEqual(prododuct.description, 'description')
        self.assertEqual(prododuct.price, 500)
    
    def tearDown(self) -> None:
        media_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'shop')
        image_list = []
        for file in os.listdir(media_folder):
            if 'test_file' in file:
                image_list.append(file)

        for i in image_list:
            os.remove(path=media_folder + '\\' + i)
        
class HomePageViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_page_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/home.html')

    def test_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class SearchResultViewTestCase(TestCase):
    
    
    def setUp(self) -> None:
        file_content = b'test_file'
        file_name = 'test_file.png'
        self.upload_file = SimpleUploadedFile(file_name, file_content, content_type='image/png')
        self.url = reverse('search-result')
        self.product1 = Product.objects.create(name='product1', description='description', price=100, image=self.upload_file)
        self.product2 = Product.objects.create(name='product2', description='description', price=200, image=self.upload_file)
        

    def test_search_without_sort(self):
        response = self.client.get(self.url, {'q': 'product1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product1')
        self.assertNotContains(response, 'product2')


    def test_search_with_sort(self):
        params = {'q': 'product', 'sort-by': 'price'}
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product1')
        self.assertContains(response, 'product2')
        self.assertQuerysetEqual(
            response.context['products'], 
            [self.product1, self.product2], 
            ordered=False
        )

    def test_sort_without_search(self):
        response = self.client.get(self.url, {'sort-by': 'price'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product1')
        self.assertContains(response, 'product2')
        self.assertQuerysetEqual(
            response.context['products'], 
            [self.product1, self.product2], 
            ordered=False
        )

    def test_no_search_no_sort(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product1')
        self.assertContains(response, 'product2')
        self.assertQuerysetEqual(
            response.context['products'], 
            [self.product1, self.product2], 
            ordered=False
        )
    
    def tearDown(self) -> None:
        media_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'shop')
        image_list = []
        for file in os.listdir(media_folder):
            if 'test_file' in file:
                image_list.append(file)

        for i in image_list:
            os.remove(path=media_folder + '\\' + i)