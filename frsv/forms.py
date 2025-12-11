from django import forms
from .models import PeopleEmb

class RegisterForm(forms.Form):

    class Meta:
        model = PeopleEmb
        fields = ['image', 'name', 'last_name']
