from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, OTPVerificationForm
from .utils import create_otp, send_otp_email, verify_otp


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

            else:

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )

                user.is_active = False
                user.save()

            otp = create_otp(user)

            send_otp_email(
                user,
                otp
            )

            request.session["otp_user_id"] = user.id
            request.session["otp_purpose"] = "signup"

            messages.success(
                request,
                "Verification code sent to your email."
            )

            return redirect("verify_otp")

    else:

        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        if not email:

            messages.error(
                request,
                "Please enter your email address."
            )

            return redirect("login")

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "No account found with this email. Please sign up first."
            )

            return redirect("login")

        otp = create_otp(user)

        send_otp_email(
            user,
            otp
        )

        request.session["otp_user_id"] = user.id
        request.session["otp_purpose"] = "login"

        messages.success(
            request,
            "Login verification code sent to your email."
        )

        return redirect("verify_otp")

    return render(request, "login.html")


def verify_otp_view(request):

    user_id = request.session.get(
        "otp_user_id"
    )

    purpose = request.session.get(
        "otp_purpose"
    )

    if not user_id or not purpose:

        messages.error(
            request,
            "Your verification session has expired."
        )

        return redirect("login")

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        request.session.flush()

        messages.error(
            request,
            "User account not found."
        )

        return redirect("signup")

    if request.method == "POST":

        form = OTPVerificationForm(
            request.POST
        )

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            success, message = verify_otp(
                user,
                entered_otp
            )

            if success:

                user.is_active = True

                user.save(
                    update_fields=["is_active"]
                )

                login(
                    request,
                    user
                )

                request.session.pop(
                    "otp_user_id",
                    None
                )

                request.session.pop(
                    "otp_purpose",
                    None
                )

                messages.success(
                    request,
                    "Authentication successful."
                )

                return redirect(
                    "dashboard"
                )

            messages.error(
                request,
                message
            )

    else:

        form = OTPVerificationForm()

    return render(
        request,
        "verify_otp.html",
        {"form": form, "email": user.email, "purpose": purpose},
    )


def resend_otp_view(request):

    if request.method != "POST":
        return redirect("verify_otp")

    user_id = request.session.get("otp_user_id")
    purpose = request.session.get("otp_purpose")

    if not user_id or not purpose:
        messages.error(request, "Your verification session has expired.")
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, "User account not found.")
        return redirect("signup")

    otp = create_otp(user)
    send_otp_email(user, otp)
    messages.success(request, "A new verification code was sent to your email.")
    return redirect("verify_otp")


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