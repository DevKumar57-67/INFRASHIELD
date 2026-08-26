from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import EmailOTP
from .utils import create_otp, verify_otp


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AuthenticationFlowTests(TestCase):

	def test_public_pages_render(self):
		for route in ("splash", "signup", "login"):
			response = self.client.get(reverse(route))
			self.assertEqual(response.status_code, 200)

	def test_dashboard_redirects_to_login_for_anonymous_users(self):
		response = self.client.get(reverse("dashboard"))
		self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

	def test_signup_sends_otp_and_verify_logs_user_in(self):
		response = self.client.post(reverse("signup"), {
			"first_name": "Ada",
			"last_name": "Lovelace",
			"email": "Ada@example.com",
		})

		self.assertRedirects(response, reverse("verify_otp"))
		user = User.objects.get(email="ada@example.com")
		self.assertFalse(user.is_active)
		self.assertEqual(len(mail.outbox), 1)

		otp = mail.outbox[0].body.splitlines()[5].strip()
		response = self.client.post(reverse("verify_otp"), {"otp": otp})

		self.assertRedirects(response, reverse("dashboard"))
		self.assertTrue(User.objects.get(pk=user.pk).is_active)

	def test_resend_replaces_existing_otp(self):
		user = User.objects.create_user(
			username="user@example.com", email="user@example.com"
		)
		session = self.client.session
		session["otp_user_id"] = user.id
		session["otp_purpose"] = "login"
		session.save()
		create_otp(user)

		response = self.client.post(reverse("resend_otp"))

		self.assertRedirects(response, reverse("verify_otp"))
		self.assertEqual(EmailOTP.objects.filter(user=user).count(), 1)
		self.assertEqual(len(mail.outbox), 1)

	def test_otp_expires_and_limits_attempts(self):
		user = User.objects.create_user(
			username="user@example.com", email="user@example.com"
		)
		create_otp(user)
		record = EmailOTP.objects.get(user=user)
		record.expires_at = timezone.now() - timedelta(seconds=1)
		record.save(update_fields=["expires_at"])
		self.assertEqual(verify_otp(user, "123456"), (False, "OTP has expired."))

		create_otp(user)
		with patch("accounts.utils.check_password", return_value=False):
			for _ in range(5):
				self.assertEqual(verify_otp(user, "123456"), (False, "Invalid OTP."))
			self.assertEqual(
				verify_otp(user, "123456"),
				(False, "Too many attempts. Please request a new OTP."),
			)
		self.assertEqual(verify_otp(user, "123456"), (False, "No active OTP found."))

# Create your tests here.
