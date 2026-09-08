from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib import messages
from .forms import DeleteAccountForm
from django.contrib.auth.decorators import login_required


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


@login_required
def delete_user(request: HttpRequest):
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get('password')
            if user.check_password(current_password):
                logout(request)
                user.delete()
                messages.success(request,"Contul tău a fost șters definitiv. Rețetele tale au fost păstrate în comunitate.")
                return redirect("home")
            else:
                messages.error(request, "Parola introdusă este incorectă! Contul nu a fost șters.")
    else:
        form = DeleteAccountForm()
    return render(request, 'accounts/delete_confirm.html', {"form": form})

