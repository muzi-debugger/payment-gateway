from django.shortcuts import render
from django.shortcuts import redirect, render

from ClickPay import settings
from .forms import MerchantForm
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def merchants(request):
    return render(request, 'register.html')

def merchant_register(request):
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            merchant = form.save(commit=False)
            
            # Create Stripe account
            account = stripe.Account.create(
                type="express",
                email=merchant.email,
                business_type="individual",
            )
            merchant.stripe_account_id = account.id
            merchant.save()

            # Generate Stripe onboarding link
            account_link = stripe.AccountLink.create(
                account=merchant.stripe_account_id,
                refresh_url=request.build_absolute_uri('/refresh'),
                return_url=request.build_absolute_uri('/success'),
                type="account_onboarding",
            )
            return redirect(account_link.url)
    else:
        form = MerchantForm()
    return render(request, 'merchant_register.html', {'form': form})
