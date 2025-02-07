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
from customers.models import Customer

# Set the Stripe secret key correctly
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

def payments(request):
    return JsonResponse({'message': 'Payments endpoint'})

@csrf_exempt
@login_required
def create_checkout_session(request, product_id):  
    try:
        # Get the user (logged-in user)
        user = request.user

        # Ensure the customer exists or create it
        customer, created = Customer.objects.get_or_create(user=user)

        # If the customer was created, create the Stripe customer and associate it
        if created:
            stripe_customer = stripe.Customer.create(email=user.email)
            customer.stripe_customer_id = stripe_customer.id  # Save the Stripe customer ID
            customer.save()
        else:
            # Fetch the existing Stripe customer ID
            stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)

        # Get the product from the database
        product = Product.objects.get(id=product_id)  # Get the product by ID

        # Create an order instance
        order = Order.objects.create(
            product=product,  # Associate the product with the order
            buyer_email=user.email,  # Store the buyer's email
            customer=customer  # Associate the customer object
        )

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {  # Price data
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                        #'images': [product.image.url],  # Product image URL
                    },
                    'unit_amount': int(product.price),  # Convert price to cents
                },
                'quantity': 1,
            }],
            metadata={  # Metadata (tracking data)
                'order_id': order.id,
                'email': user.email,
                'product_name': product.name,
                'product_id': product.id,  # Include the product ID
                'customer_name': user.get_full_name(),  # Use the user's name
            },
            mode='payment',
            success_url=settings.SUCCESS_URL,
            cancel_url=settings.CANCEL_URL,
            customer=stripe_customer.id,  # Use the Stripe customer ID here
        )
        # print success url
        

        # Return the session URL to redirect the user to Stripe Checkout
        return JsonResponse({'url': session.url})

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error creating Stripe session: {e}")
        return JsonResponse({'error': 'Could not create checkout session'}, status=500)



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

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')