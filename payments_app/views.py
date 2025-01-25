from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from merchants.models import Merchant
import stripe
from django.views.decorators.csrf import csrf_exempt

from payments_app.models import Payments
from django.http import JsonResponse

# Create your views here.

def payments(request):
    return render(request, 'payments.html')

def create_payment_intent(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        payment_amount = request.POST.get("amount")

        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(payment_amount) * 100),
            currency="usd",
            payment_method_types=["card"],
            transfer_data={"destination": merchant.stripe_account_id},
        )
        return JsonResponse({"client_secret": payment_intent.client_secret})
    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)
    

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        # Update payment status in the database
        Payments.objects.filter(stripe_payment_intent_id=payment_intent["id"]).update(
            status="Completed"
        )

    return JsonResponse({"status": "success"})

