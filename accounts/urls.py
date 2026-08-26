from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.splash,
        name="splash"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "verify-otp/",
        views.verify_otp_view,
        name="verify_otp"
    ),

    path(
        "resend-otp/",
        views.resend_otp_view,
        name="resend_otp"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
]