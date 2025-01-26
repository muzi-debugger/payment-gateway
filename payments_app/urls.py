from django.urls import path
from .views import payments, create_payment_intent, stripe_webhook

app_name = 'payments_app'

urlpatterns = [
    path('', payments, name='payments'),
    path('create-payment-intent/<int:merchant_id>/', create_payment_intent, name='create_payment_intent'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]
