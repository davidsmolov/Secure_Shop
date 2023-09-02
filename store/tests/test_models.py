from django.test import TestCase
from store.models import *
from accounts.models import CustomUser

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=10.0, description="Test Description", stock=5)

    def test_product_str(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(str(product), "Test Product")

    def test_product_price(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 10.0)

    def test_product_description(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description, "Test Description")

    def test_product_stock(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.stock, 5)

    def test_product_available(self):
        product = Product.objects.get(name="Test Product")
        self.assertTrue(product.available)
        
        
class CartTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='unitest@test.com', password='testpass')
        self.product1 = Product.objects.create(name='Test Product 1', price=10.0, description='Test Description', stock=5)
        self.product2 = Product.objects.create(name='Test Product 2', price=5.0, description='Test Description2', stock=5)
        self.cart = Cart.objects.create(owner=self.user, total=0)

    def test_cart_str(self):
        cart = Cart.objects.get(owner=self.user)
        self.assertEqual(str(cart), f'Cart {cart.pk}, at a total of {cart.total}')

    def test_cart_total_price(self):
        cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)
        self.assertEqual(self.cart.total_price(), 35.0)