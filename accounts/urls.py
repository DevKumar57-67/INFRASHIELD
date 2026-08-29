from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    path("settings/",
    views.settings_view,
    name="settings"
    ),


    path(
    "report/",
    views.create_report,
    name="create_report"
),


path(
    "feed/",
    views.infrastructure_feed,
    name="infrastructure_feed"
),

path(
    "report/<int:report_id>/confirm/",
    views.confirm_report,
    name="confirm_report"
),

path(
    "report/<int:report_id>/comment/",
    views.add_comment,
    name="add_comment"
),


path(
    "my-reports/",
    views.my_reports,
    name="my_reports"
),








]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)