from django import forms
from .models import PeopleEmb

class RegisterForm(forms.ModelForm):

    class Meta:
        model = PeopleEmb
        fields = ['name','image']
