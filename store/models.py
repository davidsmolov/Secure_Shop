from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [('can_change_products', 'Can change products')]
    
class Cart(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem', related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Cart {self.pk}, at a total of {self.total}'
    
    def total_price(self):
        total = 0
        for item in self.cart_items.all():
            total += item.product.price * item.quantity
        return total
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Cart {self.cart.pk}'