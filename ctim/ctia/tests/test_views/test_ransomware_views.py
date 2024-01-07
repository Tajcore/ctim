# ctim/ctia/tests/test_views/test_ransomware_views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test.utils import ignore_warnings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ctim.ctia.models.ransomware import Group, Location, Post, Profile

ignore_warnings(message="No directory at", module="sentry_sdk").enable()

User = get_user_model()


class BaseViewSetTest(APITestCase):
    def setUp(self, permission_required):
        # Create a test user
        self.user = User.objects.create_user(password="testpassword", email="test@test.com")
        permission_to_add = Permission.objects.get(codename=permission_required, content_type__app_label="ctia")
        self.user.user_permissions.add(permission_to_add)
        self.user.save()


class GroupViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp("view_group")
        self.group = Group.objects.create(name="Test Group")

    def test_group_list(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("group-list"))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_group_retrieve(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("group-detail", kwargs={"pk": self.group.pk}))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Group")


class LocationViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp("view_location")
        self.group = Group.objects.create(name="Test Group")
        self.location = Location.objects.create(
            group=self.group, fqdn="example.com", version=1, available=True, lastscrape=timezone.now(), enabled=True
        )

    def test_location_list(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("location-list"))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_location_retrieve(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("location-detail", kwargs={"pk": self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("example.com", response.data["fqdn"])


class ProfileViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp("view_profile")
        self.group = Group.objects.create(name="Test Group")
        self.profile = Profile.objects.create(group=self.group, url="http://example.com/profile")

    def test_profile_list(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("profile-list"))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_profile_retrieve(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("profile-detail", kwargs={"pk": self.profile.pk}))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("http://example.com/profile", response.data["url"])


class PostViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp("view_post")
        self.group = Group.objects.create(name="Test Group")
        self.post = Post.objects.create(
            title="Test Post",
            group=self.group,
            discovered=timezone.now(),
            url="http://example.com/post",
            country="Test Country",
            published=timezone.now(),
        )

    def test_post_list(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("post-list"))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_retrieve(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse("post-detail", kwargs={"pk": self.post.pk}))
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")
