from django.shortcuts import render
from django.shortcuts import redirect, render
from .forms import MerchantForm

# Create your views here.
def merchants(request):
    return render(request, 'register.html')

def merchant_register(request):
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = MerchantForm()
    return render(request, 'merchant_register.html', {'form': form})