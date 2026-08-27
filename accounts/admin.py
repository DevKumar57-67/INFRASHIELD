from django.contrib import admin
from .models import InfrastructureReport


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