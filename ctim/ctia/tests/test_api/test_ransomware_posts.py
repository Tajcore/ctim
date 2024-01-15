from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ctim.ctia.models.ransomware import Group, Post

User = get_user_model()


class PostAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(password="testpassword", email="test@test.com")
        view_group_permission = Permission.objects.get(codename="view_post", content_type__app_label="ctia")
        self.user.user_permissions.add(view_group_permission)
        self.user.save()

        # Creating a sample group and posts for testing
        group = Group.objects.create(name="Test Group")
        Post.objects.create(
            title="Post 1",
            group=group,
            discovered=timezone.now(),
            published=timezone.now(),
            url="http://example.com/post1",
            country="Country 1",
        )
        Post.objects.create(
            title="Post 2",
            group=group,
            discovered=timezone.now(),
            published=timezone.now(),
            url="http://example.com/post2",
            country="Country 2",
        )

    def test_post_list(self):
        url = reverse("post-list")
        self.client.force_authenticate(user=self.user)  # Force authentication
        response = self.client.get(url)
        self.client.force_authenticate(user=None)  # Reset authentication

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIn("Post 1", [post["title"] for post in response.data["results"]])

    def test_post_detail(self):
        post = Post.objects.get(title="Post 1")
        url = reverse("post-detail", kwargs={"pk": post.pk})
        self.client.force_authenticate(user=self.user)  # Force authentication
        response = self.client.get(url)
        self.client.force_authenticate(user=None)  # Reset authentication

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Post 1")
