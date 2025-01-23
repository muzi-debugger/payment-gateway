from django.urls import path
from .views import payments
from django.contrib.auth import views as auth_views

app_name = 'payments_app'

urlpatterns = [
    path('payments/', payments, name='payments'),
]