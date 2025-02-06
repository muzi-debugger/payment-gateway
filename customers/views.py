from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)
        else:
            return render(request,'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html', {'error': 'Invalid email or password'})

