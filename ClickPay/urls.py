from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views 
from . import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.home_page, name='home_page'),
    path('customers/', include('customers.urls')),
    path('payments/', include('payments_app.urls')),
    
]
