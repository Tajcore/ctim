# ctim/ctia/tests/test_api/test_ransomware_groups.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ctim.ctia.models.ransomware import Group

User = get_user_model()


class GroupAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(password="testpassword", email="test@test.com")
        view_group_permission = Permission.objects.get(codename="view_group", content_type__app_label="ctia")
        self.user.user_permissions.add(view_group_permission)
        self.user.save()

        # Creating sample groups for testing
        Group.objects.create(name="Group 1")
        Group.objects.create(name="Group 2")

    def test_group_list(self):
        url = reverse("group-list")
        self.client.force_authenticate(user=self.user)  # Force authentication
        response = self.client.get(url)
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIn("Group 1", [group["name"] for group in response.data["results"]])

    def test_group_detail(self):
        group = Group.objects.get(name="Group 1")
        url = reverse("group-detail", kwargs={"pk": group.pk})
        self.client.force_authenticate(user=self.user)  # Force authentication
        response = self.client.get(url)
        self.client.force_authenticate(user=None)  # Reset authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Group 1")
