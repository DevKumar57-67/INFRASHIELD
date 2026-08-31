from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse


class AuthenticationFlowTests(TestCase):

	def test_public_pages_render(self):
		for route in ("splash", "signup", "login"):
			response = self.client.get(reverse(route))
			self.assertEqual(response.status_code, 200)

	def test_dashboard_redirects_to_login_for_anonymous_users(self):
		response = self.client.get(reverse("dashboard"))
		self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

	def test_signup_creates_active_user_and_redirects_to_login(self):
		response = self.client.post(reverse("signup"), {
			"first_name": "Ada",
			"last_name": "Lovelace",
			"email": "Ada@example.com",
			"password": "correct-horse-battery",
			"password_confirmation": "correct-horse-battery",
		})

		self.assertRedirects(response, reverse("login"))
		user = User.objects.get(email="ada@example.com")
		self.assertTrue(user.is_active)
		self.assertTrue(user.check_password("correct-horse-battery"))

	def test_login_with_password_redirects_to_dashboard(self):
		User.objects.create_user(
			username="ada@example.com",
			email="ada@example.com",
			password="correct-horse-battery",
		)

		response = self.client.post(reverse("login"), {
			"email": "ADA@example.com",
			"password": "correct-horse-battery",
		})

		self.assertRedirects(response, reverse("dashboard"))

	def test_login_with_invalid_password_stays_on_login(self):
		User.objects.create_user(
			username="ada@example.com",
			email="ada@example.com",
			password="correct-horse-battery",
		)

		response = self.client.post(reverse("login"), {
			"email": "ada@example.com",
			"password": "wrong-password",
		})

		self.assertRedirects(response, reverse("login"))

	def test_media_url_is_registered(self):
		self.assertIsNotNone(resolve("/media/"))

# Create your tests here.
