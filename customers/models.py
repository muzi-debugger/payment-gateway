from django.db import models
from django import forms
class Customer(models.Model):
    customer_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    