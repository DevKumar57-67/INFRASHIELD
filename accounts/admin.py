from django.contrib import admin
from .models import InfrastructureReport, Profile
from .models import InfrastructureReport, Profile, UserSettings

@admin.register(InfrastructureReport)
class InfrastructureReportAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "infrastructure_type",
        "location",
        "risk_level",
        "created_at",
    )

    list_filter = (
        "infrastructure_type",
        "risk_level",
        "created_at",
    )

    search_fields = (
        "title",
        "location",
        "description",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "location",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "location",
    )

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "risk_alerts",
        "report_updates",
        "system_notifications",
        "theme",
        "language",
        "default_map_view",
    )

    search_fields = (
        "user__username",
        "user__email",
    )