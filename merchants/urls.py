from django.urls import path
from .views import merchants
from django.contrib.auth import views as auth_views
from . import views

app_name = 'merchants'

urlpatterns = [
    path('', views.merchant_register, name='merchant_register'),
]
