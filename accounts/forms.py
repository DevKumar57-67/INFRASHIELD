from django import forms
from django.core.validators import RegexValidator


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address"
        })
    )


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        validators=[RegexValidator(r"^\d{6}$", "Enter a valid 6-digit OTP.")],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter 6-digit OTP"
        })
    )