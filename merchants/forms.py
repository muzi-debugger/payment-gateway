from django import forms
from .models import Merchant

class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ('name', 'surname', 'email', 'phone')
    industires = forms.ChoiceField(choices=[
        ('automotive', 'Automotive'),
        ('construction', 'Construction'),
        ('electronics', 'Electronics'),
        ('food', 'Food'),
        ('furniture', 'Furniture'),
        ('gardening', 'Gardening'),
        ('grocery', 'Grocery'),
        ('health', 'Health'),
        ('home', 'Home'),
        ('insurance', 'Insurance'),
        ('lawn', 'Lawn'),
        ('medical', 'Medical'),
        ('office', 'Office'),
        ('other', 'Other'),
        ('pet', 'Pet'),
        ('pharmacy', 'Pharmacy'),
        ('real_estate', 'Real Estate'),
        ('retail', 'Retail'),
        ('sports', 'Sports'),
        ('telecommunications', 'Telecommunications'),
        ('travel', 'Travel'),
        ('wholesale', 'Wholesale'),
        ('wine', 'Wine'),
        ('other', 'Other'),
    ])
    location =forms.ChoiceField(choices=[
            ('Gauteng', 'Gauteng'),
            ('KwaZulu-Natal', 'KwaZulu-Natal'),
            ('Limpopo', 'Limpopo'),
            ('Mpumalanga', 'Mpumalanga'),
            ('North West', 'North West'),
            ('Northern Cape', 'Northern Cape'),
            ('Eastern Cape', 'Eastern Cape'),
            ('Western Cape', 'Western Cape'),
            ('Free State', 'Free State'),
            ])