import secrets
from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

from .models import EmailOTP


def generate_otp():
    """
    Generate a secure 6-digit OTP.
    """
    return f"{secrets.randbelow(900000) + 100000}"


def create_otp(user):
    """
    Create a new OTP for the user.
    """

    # Remove previous OTPs
    EmailOTP.objects.filter(user=user).delete()

    # Generate OTP
    otp = generate_otp()

    # Hash OTP before storing it
    hashed_otp = make_password(otp)

    # Create OTP record
    otp_record = EmailOTP.objects.create(
        user=user,
        otp=hashed_otp,
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    return otp


def verify_otp(user, entered_otp):
    """
    Verify the OTP entered by the user.
    """

    otp_record = EmailOTP.objects.filter(
        user=user,
        is_verified=False
    ).order_by("-created_at").first()

    if not otp_record:
        return False, "No active OTP found."

    # Check expiry
    if timezone.now() > otp_record.expires_at:
        otp_record.delete()
        return False, "OTP has expired."

    # Maximum attempts
    if otp_record.attempts >= 5:
        otp_record.delete()
        return False, "Too many attempts. Please request a new OTP."

    # Increase attempt count
    otp_record.attempts += 1
    otp_record.save(update_fields=["attempts"])

    # Verify hashed OTP
    if check_password(entered_otp, otp_record.otp):

        otp_record.is_verified = True
        otp_record.save(update_fields=["is_verified"])

        return True, "OTP verified successfully."

    return False, "Invalid OTP."


def send_otp_email(user, otp):
    """
    Send OTP to user's email.
    """

    subject = "Your Infra Shield Verification Code"

    message = f"""
Hello {user.first_name},

Your Infra Shield verification code is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this code, please ignore this email.

Regards,
Infra Shield Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )