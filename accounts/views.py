from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm


def splash(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "splash.html")


def signup(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]

            existing_user = User.objects.filter(
                email=email
            ).first()

            if existing_user:

                if existing_user.is_active:

                    messages.error(
                        request,
                        "An account with this email already exists."
                    )

                    return redirect("login")

                user = existing_user
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password)
                user.is_active = True
                user.save()

            else:

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )

            messages.success(
                request,
                "Account created. Please log in."
            )

            return redirect("login")

    else:

        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html")


@login_required
def dashboard(request):

    return render(request, "dashboard.html")


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("splash")