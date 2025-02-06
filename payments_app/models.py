from django.db import models
from django.db import models    
import stripe

from customers.models import Customer
from products.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_email = models.EmailField(max_length=255)
    total_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=255, default="pending")
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

def __str__(self):
    return f"Payment {self.id}"
