from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm


def login_user(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
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
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {"form":form})

def logout_user(request: HttpRequest):
    logout(request)
    return redirect('home')
