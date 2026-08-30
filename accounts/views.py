from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InfrastructureReportForm, SignupForm
from .models import (
    InfrastructureReport,
    Profile,
    ReportComment,
    ReportConfirmation,
    UserSettings,
)


# ==============================
# SPLASH PAGE
# ==============================

def splash(request):
    if request.user.is_authenticated:
        return redirect("infrastructure_feed")
    return render(request, "splash.html")


# ==============================
# SIGNUP
# ==============================

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

            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                if existing_user.is_active:
                    messages.error(request, "An account with this email already exists.")
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

            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


# ==============================
# LOGIN
# ==============================

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
        return redirect("infrastructure_feed")

    return render(request, "login.html")


# ==============================
# DASHBOARD
# ==============================

@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "page_title": "Dashboard",
            "page_search_placeholder": "Search city, road, bridge or location...",
        },
    )


# ==============================
# PROFILE
# ==============================

@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        profile.location = request.POST.get("location", "").strip()
        profile.phone = request.POST.get("phone", "").strip()
        profile.bio = request.POST.get("bio", "").strip()

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        user.save()
        profile.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "profile": profile,
            "page_title": "Profile",
        },
    )


@login_required
@login_required
def settings(request):

    settings, created = UserSettings.objects.get_or_create(
        user=request.user
    )

    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        settings.risk_alerts = (
            "risk_alerts" in request.POST
        )

        settings.report_updates = (
            "report_updates" in request.POST
        )

        settings.system_notifications = (
            "system_notifications" in request.POST
        )

        settings.theme = request.POST.get(
            "theme",
            "dark"
        )

        settings.language = request.POST.get(
            "language",
            "English"
        )

        settings.default_map_view = request.POST.get(
            "default_map_view",
            "standard"
        )

        settings.save()

        messages.success(
            request,
            "Settings updated successfully."
        )

        return redirect("settings")

    return render(
        request,
        "settings.html",
        {
            "settings": settings,
            "profile": profile
        }
    )

# ==============================
# LOGOUT
# ==============================

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("splash")


# ==============================
# REPORTS
# ==============================

@login_required
def create_report(request):
    if request.method == "POST":
        form = InfrastructureReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Infrastructure report submitted successfully.")
            return redirect("infrastructure_feed")
    else:
        form = InfrastructureReportForm()

    return render(
        request,
        "create_report.html",
        {
            "form": form,
            "page_title": "Report Issue",
        },
    )


@login_required
def confirm_report(request, report_id):
    if request.method != "POST":
        return redirect("infrastructure_feed")

    report = get_object_or_404(InfrastructureReport, id=report_id)
    confirmation, created = ReportConfirmation.objects.get_or_create(report=report, user=request.user)

    if created:
        messages.success(request, "You confirmed this infrastructure issue.")
    else:
        confirmation.delete()
        messages.info(request, "Your confirmation was removed.")

    return redirect("infrastructure_feed")


@login_required
def add_comment(request, report_id):
    if request.method != "POST":
        return redirect("infrastructure_feed")

    report = get_object_or_404(InfrastructureReport, id=report_id)
    content = request.POST.get("content", "").strip()

    if not content:
        messages.error(request, "Comment cannot be empty.")
        return redirect("infrastructure_feed")

    if len(content) > 1000:
        messages.error(request, "Comment cannot exceed 1000 characters.")
        return redirect("infrastructure_feed")

    ReportComment.objects.create(report=report, user=request.user, content=content)
    messages.success(request, "Comment added successfully.")
    return redirect("infrastructure_feed")


@login_required
def infrastructure_feed(request):
    reports = (
        InfrastructureReport.objects.select_related("user")
        .prefetch_related("confirmations", "comments__user")
        .order_by("-created_at")
    )
    return render(
        request,
        "infrastructure_feed.html",
        {
            "reports": reports,
            "page_title": "Infrastructure Feed",
        },
    )


@login_required
def my_reports(request):
    reports = InfrastructureReport.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request,
        "my_reports.html",
        {
            "reports": reports,
            "page_title": "My Reports",
        },
    )


@login_required
def risk_map_view(request):
    return render(request, "risk_map.html", {"page_title": "Risk Map"})


@login_required
def analytics_view(request):
    return render(request, "analytics.html", {"page_title": "Analytics"})

