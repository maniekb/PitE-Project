from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'register.html', {'form': form})

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')
