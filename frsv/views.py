from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request , 'frsv:index')
        

    else:
        form = RegisterForm()

    