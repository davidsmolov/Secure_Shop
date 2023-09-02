from django.db import models
from accounts.models import CustomUser
from store.models import *

# Create your models here.
    
 
class PayPalOrder(models.Model):
    payment_id = models.CharField(max_length=120)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.payment_id