from allauth.socialaccount.models import SocialAccount, SocialApp
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test.utils import ignore_warnings
from django.urls import reverse
from rest_framework.test import APITestCase

ignore_warnings(message="No directory at", module="sentry_sdk").enable()

User = get_user_model()


class SocialSignupTest(APITestCase):
    def setUp(self):
        # Common setup code
        user = User.objects.create_user(email="testuser@test.com", password="12345")
        site = Site.objects.get_current()
        site.domain = "testserver"
        site.name = "Test Server"
        site.save()

        social_apps = [
            {"provider": "github", "name": "GitHub", "client_id": "github_client_id", "secret": "github_secret"},
            {"provider": "google", "name": "Google", "client_id": "google_client_id", "secret": "google_secret"},
        ]

        for app in social_apps:
            social_app = SocialApp.objects.create(**app)
            social_app.sites.add(site)
            SocialAccount.objects.create(user=user, provider=app["provider"], uid=f"{app['provider']}_123")

    def check_social_links(self, url, provider_classes):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")
        for provider_class in provider_classes:
            link = soup.find("a", class_=provider_class)
            self.assertIsNotNone(link, f"{provider_class} login link is missing from the page")
            self.assertTrue(hasattr(link, "href"), f"{provider_class} link does not have an href attribute")

    def check_social_links_not_present(self, url, provider_classes):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")
        for provider_class in provider_classes:
            link = soup.find("a", class_=provider_class)
            self.assertIsNone(link, f"{provider_class} login link is unexpectedly present on the page")

    def test_social_login_links_present_signup(self):
        self.check_social_links_not_present(
            reverse("account_signup"), ["socialaccount_provider github", "socialaccount_provider google"]
        )

    def test_social_login_links_present_login(self):
        self.check_social_links(
            reverse("account_login"), ["socialaccount_provider github", "socialaccount_provider google"]
        )
