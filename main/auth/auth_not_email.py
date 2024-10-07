from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from main.models import User


def login_view(request):
    """Аутентификация"""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            username = username.lower()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.add_message(
                    request, messages.INFO, "НЕПРАВИЛЬНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЛИ ПАРОЛЬ"
                )
                return redirect("login")
        except:
            messages.add_message(request, messages.INFO, "ОШИБКА!")
            return redirect("login_")
    return render(request, "register_views/login.html")


def register_view(request):
    """Регистрация"""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            username = username.lower()
            password = make_password(password)
            user = User(username=username, password=password)
            user.save()
            # return redirect("register")
            return redirect("login_")
        except:
            messages.add_message(request, messages.INFO, "ОШИБКА!")
            return redirect("register")

    return render(request, "register_views/register.html")


def logoutPage(request):
    """Выход"""

    logout(request)
    return redirect("/")
