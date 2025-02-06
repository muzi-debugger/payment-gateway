from django.urls import path
from .views import payments, stripe_webhook, create_checkout_session, order_view 

app_name = 'payments_app'

urlpatterns = [
    path('', payments, name='payments'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('order/<int:product_id>', order_view, name='order'),
    path("create-checkout-session/<int:product_id>", create_checkout_session, name="create-checkout-session"),
    
]

