from django.urls import path
from .views import customer_registration as register_customer
from django.contrib.auth import views as auth_views

app_name = 'customers'

urlpatterns = [
    path('customer_registration/', register_customer, name='customer_registration'),
]