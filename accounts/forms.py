from django import forms
from .models import InfrastructureReport


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

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )

    password_confirmation = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirmation"):
            self.add_error("password_confirmation", "Passwords do not match.")
        return cleaned_data






class InfrastructureReportForm(forms.ModelForm):

    class Meta:

        model = InfrastructureReport

        fields = [
            "infrastructure_type",
            "title",
            "description",
            "image",
            "location",
            "latitude",
            "longitude",
        ]

        widgets = {

            "infrastructure_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Large crack detected on road"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the infrastructure issue...",
                    "rows": 5
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Lucknow, Uttar Pradesh"
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 26.8467",
                    "step": "any"
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 80.9462",
                    "step": "any"
                }
            ),
        }

