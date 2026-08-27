from django.db import models
from django.contrib.auth.models import User


class InfrastructureReport(models.Model):

    INFRASTRUCTURE_TYPES = [
        ("road", "Road"),
        ("bridge", "Bridge"),
        ("railway", "Railway"),
        ("building", "Building"),
        ("street", "Street Infrastructure"),
        ("drainage", "Drainage"),
        ("other", "Other"),
    ]

    RISK_LEVELS = [
        ("pending", "Pending Analysis"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="infrastructure_reports"
    )

    infrastructure_type = models.CharField(
        max_length=30,
        choices=INFRASTRUCTURE_TYPES
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="infrastructure_reports/"
    )

    location = models.CharField(
        max_length=255
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default="pending"
    )

    ai_confidence = models.FloatField(
        null=True,
        blank=True
    )

    ai_analysis = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.title} - {self.infrastructure_type}"


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        max_length=500,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username