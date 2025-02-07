from django.db import models
from django.db import models    
import stripe

from customers.models import Customer
from products.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_email = models.EmailField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer
    status = models.CharField(max_length=20, default='Pending')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    

def __str__(self):
    return f"Payment {self.id}"
