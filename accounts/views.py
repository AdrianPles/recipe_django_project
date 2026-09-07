from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib import messages


def login_user(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Conectare cu succes!")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {"form":form})

def register_user(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Felicitări, {user}! Contul tău a fost creat cu succes!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {"form":form})

def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, f"Deconectare cu succes!")
    return redirect('home')
