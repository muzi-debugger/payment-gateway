from django.db import models
import stripe 
# Create your models here.
class Province(models.TextChoices):
    GAUTENG = 'Gauteng'
    KWAZULU_NATAL = 'KwaZulu-Natal'
    LIMPOPO = 'Limpopo'
    MPUMALANGA = 'Mpumalanga'
    NORTH_WEST = 'North West'
    NORTHERN_CAPE = 'Northern Cape'
    EASTERN_CAPE = 'Eastern Cape'
    WESTERN_CAPE = 'Western Cape'
    FREE_STATE = 'Free State'
    
class Merchant(models.Model):
    stripe_customer_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    Province = models.CharField(max_length=25, choices=Province.choices)


    def __str__(self):
        return self.value