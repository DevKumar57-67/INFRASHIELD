from django.contrib import admin

from .models import EmailOTP


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
	list_display = ("user", "created_at", "expires_at", "is_verified", "attempts")
	list_filter = ("is_verified",)
	search_fields = ("user__email",)
