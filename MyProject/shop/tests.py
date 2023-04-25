from django.test import TestCase, Client

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product, ProductCategory
from .views import *

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
uploaded = SimpleUploadedFile('test_gif.gif', small_gif, content_type='image/gif')

class ProductTests(TestCase):

    def setUp(self):
        ProductCategory.objects.create(category='category name')
        category = ProductCategory.objects.get(id=1)
        Product.objects.create(name='product_name',  description='description', price=500, image=uploaded)
        c = Client()
        response = c.post('/login/', {"username": "John", "password": "123456789"})
        response.status_code

    def test_product(self):
        prododuct=Product.objects.get(id=1)
        category=ProductCategory.objects.get(id=1)
        self.assertEqual(prododuct.name, 'product_name')
        self.assertEqual(prododuct.description, 'description')
        self.assertEqual(prododuct.price, 500)

        
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
        self.url = reverse('search-result')
        self.product1 = Product.objects.create(name='product1', description='description', price=100, image=uploaded)
        self.product2 = Product.objects.create(name='product2', description='description', price=200, image=uploaded)
        

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
