from django import forms
from .models import People

class RegisterForm(forms.Form):
    image = forms.ImageField(required=True)
    name  = forms.CharField(required=True,)
    class Meta:
        model = People
        fields = ['image', 'name', 'last_name']
