from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here

def home_page(request):
    return render(request, 'home_page.html')
