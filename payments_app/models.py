from django.db import models
from django.db import models    
import stripe
# Create your models here.
class Payments(models.Model):
    id = models.BigAutoField(primary_key=True)


class Address(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True)
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

class BillingDetails(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

class Payments(models.Model):
    id = models.BigAutoField(primary_key=True)
    billing_details = models.OneToOneField(BillingDetails, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    livemode = models.BooleanField(default=False)
    metadata = models.JSONField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    us_bank_account = models.CharField(max_length=255, null=True, blank=True)

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys

def __str__(self):
    return self.id
