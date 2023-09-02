from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import *
from store.serializers import *
from django.contrib.auth.models import Group, Permission
from accounts.models import CustomUser
from accounts.serializers import UserRegistrationSerializer
from django.apps import apps
import requests
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient


class ProductsViewsTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=False,
        )

        # Create or retrieve the "Seller" group
        self.seller_group, _ = Group.objects.get_or_create(name='Seller')

        # Add the user to the "Seller" group
        self.user.groups.add(self.seller_group)

        # Create an authentication token for the user
        self.access_token = AccessToken.for_user(self.user)

        # Set the Authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # Create a product
        self.product1 = Product.objects.create( name='Test Product 1', price=10.0, stock=10, description='Test Description 1')
        self.product2 = Product.objects.create( name='Test Product 2', price=20.0, stock=20, description='Test Description 2')
        
    def test_get_all_products(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_product_by_id(self):
        url = reverse('products')
        response = self.client.get(url, {'id': self.product1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product 1')

    def test_get_nonexistent_product_by_id(self):
        url = reverse('products')
        response = self.client.get(url, {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        url = reverse('products')
        data = {'name': 'New Product', 'price': 15.0, 'stock': 20,'description':'Test Description'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        url = reverse('products')
        data = {'name': 'New Product', 'price': 'invalid', 'stock': 20}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        url = reverse('products')
        request = url+'?id='+str(self.product1.id)
        data = {'price': 12.0}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(request, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=self.product1.id).price, 12.0)

    def test_update_nonexistent_product(self):
        url = reverse('products')
        request = url+'?id='+str(999)
        data = {'price': 12.0}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(request,data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_product_with_invalid_data(self):
        url = reverse('products')
        request = url+'?id='+str(self.product1.id)
        data = {'price': 'invalid'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(request,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_product_with_invalid_id(self):
        url = reverse('products')
        request = url+'?id='+str('invalid')
        data = {'price': 12.0}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(request,data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_product_with_invalid_id(self):
        url = reverse('products')
        request = url+'?id='+str('invalid')
        data = {'price': 12.0}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(request,data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_product_without_authentication(self):
        self.user = None
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer test')
        url = reverse('products')
        request = url+'?id='+str(self.product1.id)
        data = {'price': 12.0}
        response = self.client.patch(request,data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_delete_product(self):
        url = reverse('products')
        request = url+'?id='+str(self.product1.id)
        response = self.client.delete(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_nonexistent_product(self):
        url = reverse('products')
        request = url+'?id='+str(999)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CartsViewsTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=False,
        )

        # Create an authentication token for the user
        self.access_token = AccessToken.for_user(self.user)

        # Set the Authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # Create a product
        self.product1 = Product.objects.create( name='Test Product 1', price=10.0, stock=10, description='Test Description 1')
        self.product2 = Product.objects.create( name='Test Product 2', price=20.0, stock=20, description='Test Description 2')
        
        
    def test_get_empty_cart(self):
        url = reverse('carts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_cart(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 2
        },
        {
            "product": self.product2.id,
            "quantity": 3
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_cart_with_invalid_data(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 2
        },
        {
            "product": self.product2.id,
            "quantity": "invalid"
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_cart_quantity_exeeds_stock(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 20
        },
        {
            "product": self.product2.id,
            "quantity": 30
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_cart_duplicated_product(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 2
        },
        {
            "product": self.product1.id,
            "quantity": 3
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_cart(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 2
        },
        {
            "product": self.product2.id,
            "quantity": 3
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_empty_cart(self):
        url = reverse('carts')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_cart(self):
        url = reverse('carts')
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 2
        },
        {
            "product": self.product2.id,
            "quantity": 3
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {"cart_items": [
        {
            "product": self.product1.id,
            "quantity": 5
        },
        {
            "product": self.product2.id,
            "quantity": 3
        }
    ]
}
        response = self.client.patch(url, data, format='json')
        total = self.product1.price*5 + self.product2.price*3
        self.assertEqual(response.status_code, status.HTTP_200_OK)