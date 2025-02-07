from django.urls import path
from .views import sign_up, customer_login

app_name = 'customers'

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),
    path('login/', customer_login, name='customer_login'),
]