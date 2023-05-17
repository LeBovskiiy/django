import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from users.models import *

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

class TestProductDetailView(TestCase):
    
    def setUp(self) -> None:
        self.upload_file = SimpleUploadedFile('test_file', b'Content', content_type='image/png')
        self.client = Client()
        self.product_create = Product.objects.create(name='product', description='description', price=100, image=self.upload_file)
        
    def test_get_request(self):
        self.prodcut = Product.objects.get(name='product', description='description', price=100)
        self.response = self.client.get('/prodcut/1/')
        self.assertEqual(self.response.status_code, 302)
        self.assertQuerysetEqual(self.response.context['product_detail'], [self.product])
        self.assertContains(self.response, 'product')
        self.assertEqual(self.product.name, 'product')
        self.assertEqual(self.product.description, 'description')
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.image, self.upload_file)

    def tearDown(self) -> None:
        media_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'shop')
        image_list = []
        for file in os.listdir(media_folder):
            if 'test_file' in file:
                image_list.append(file)

        for i in image_list:
            os.remove(path=media_folder + '\\' + i)

class TestBasketView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.upload_file = SimpleUploadedFile('test_file', b'Content', content_type='image/png')
        self.prodcut = Product.objects.create(name='product', description='description', price=100, image=self.upload_file)
        self.User = get_user_model()
        self.user = self.User.objects.create(
            email='test@example.com',
            password='password123',
            username='Test User',
            phone='+38093939393',
        )
        self.basket = Basket.objects.create(handler=self.user)
        self.cart_item = CartItem.objects.create(basket=self.basket, product=self.prodcut, quantity=1)        
    def test_get_request(self):
        self.response = self.client.get('/basket/')
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'product')
        self.assertQuerysetEqual(self.response.context['cart_items'], [self.cart_item])
        
    def test_user_basket(self):
        self.assertEqual(self.basket.handler, self.user)
        self.assertEqual(self.cart_item.basket, self.basket)
        self.assertEqual(self.cart_item.product, self.prodcut)
        self.assertEqual(self.cart_item.quantity, 1)

class TestProductCategorie(TestCase):

    def setUp(self):
        self.client = Client()
        self.upload_file = SimpleUploadedFile('test_file', b'Content', content_type='image/png')
        self.categorie = ProductCategory.objects.create(category='SomeCategorie')
        self.prodcut = Product.objects.create(name='product', description='description', price=100, image=self.upload_file, categories=self.categorie)

    def test_corect_init(self):
        self.assertEqual(self.categorie.category, 'SomeCategorie')
        self.assertEqual(self.prodcut.categories, self.categorie)

    def test_relation(self):
        categorie = ProductCategory.objects.get(category='SomeCategorie')
        self.assertQuerysetEqual(categorie.objects.all(), self.prodcut)

    def test_categorie_view(self):
        self.response = self.client.get('/')
        self.assertContains(self.response, 'categories')
        self.assertEqual(self.response.status_code, 200)
