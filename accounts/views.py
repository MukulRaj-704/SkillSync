from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm


@login_required
def home(request):
    return render(request, "accounts/home.html")


def registerView(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            role = form.cleaned_data.get("role")

            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            messages.success(request, "Account created successfully ✅")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password ❌")

    return render(request, "accounts/login.html")


def logoutView(request):
    logout(request)
    return redirect("login")
