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
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "profile/", 
        views.profile_view, 
        name="profile"
    ),
    
]

