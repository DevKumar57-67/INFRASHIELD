from django.db import models
from django.contrib.auth.models import User


class EmailOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_otps"
    )

    otp = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(default=False)

    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.created_at:%Y-%m-%d %H:%M:%S}"