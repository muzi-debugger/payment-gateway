from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging
from .models import Order
from products.models import Product

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Set the Stripe secret key correctly
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

def payments(request):
    return JsonResponse({'message': 'Payments endpoint'})

@csrf_exempt
@login_required
def create_checkout_session(request, product_id):  
    try:
        product = Product.objects.get(id=product_id)  # Get product from database
        # create an order instance
        order = Order.objects.create(
            product=product,  # Associate the product with the order
            buyer_email=request.user.email,  # Get the buyer's email
            customer=request.user.customer  # Get the customer associated with the buyer
        )
        # Create a checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {  # Price data
                    'currency': 'usd',  # Currency
                    'product_data': {  # Product data
                        'name': product.name,  # Product name
                        'images': [product.image.url],  # Product image URL
                    },  # Product data
                    'unit_amount': int(product.price * 100),  # Convert to cents
                },
                'quantity': 1,  # Quantity
            }],
            metadata={  # Metadata
                'order_id': order.id,  # Order ID
                'email': request.user.email,  # Buyer's email
                'product_name': product.name,  # Product name
                'customer_name': request.user.customer.name,  # Customer name
            },  # Metadata
            mode='payment',  # Mode
            success_url=settings.SUCCESS_URL,  # Success URL
            cancel_url=settings.CANCEL_URL,  # Cancel URL
            customer=request.user.customer.stripe_customer_id,  # Customer ID
        )
        return JsonResponse({'url': session.url})  # Return the checkout session URL
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error creating Stripe session: {e}")  # Log the error
        return JsonResponse({'error': 'Could not create checkout session'}, status=500)  # Return an error response


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        logger.error("Invalid webhook payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Webhook signature verification failed")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            order.status = 'Paid'
            order.stripe_payment_intent_id = session.get('payment_intent')
            order.save()
            logger.info(f"Order {order.id} marked as paid.")
        except Order.DoesNotExist:
            logger.error(f"Order ID {order_id} not found in database")

    return HttpResponse(status=200)

def order_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'order.html', {'product': product})
