import stripe
from django.shortcuts import redirect, render
from .forms import CustomerRegistrationForm
from .models import Customer
import environ

env = environ.Env()
environ.Env.read_env()

stripe.api_key = env('STRIPE_SECRET_KEY')

def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer_data = form.cleaned_data
            stripe_customer = stripe.Customer.create(
                name=customer_data['name'],
                email=customer_data['email'],
            )
            customer = Customer.objects.create(
                stripe_customer_id=stripe_customer.id,
                name=customer_data['name'],
                email=customer_data['email'],
            )
            return redirect('customers:customer_registration')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_registration.html', {'form': form})