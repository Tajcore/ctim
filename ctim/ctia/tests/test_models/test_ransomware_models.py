# ctim/ctia/tests/test_models/test_ransomware_models.py
from django.test import TestCase
from django.utils import timezone

from ctim.ctia.models.ransomware import Group, Location, Post, Profile


class GroupModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")

    def test_group_creation(self):
        self.assertEqual(self.group.name, "Test Group")


class LocationModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.location = Location.objects.create(
            group=self.group, fqdn="example.com", version=1, available=True, lastscrape=timezone.now(), enabled=True
        )

    def test_location_creation(self):
        self.assertEqual(self.location.group, self.group)
        self.assertEqual(self.location.fqdn, "example.com")
        self.assertEqual(self.location.version, 1)
        self.assertTrue(self.location.available)
        self.assertIsNotNone(self.location.lastscrape)
        self.assertTrue(self.location.enabled)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.profile = Profile.objects.create(group=self.group, url="http://example.com/profile")

    def test_profile_creation(self):
        self.assertEqual(self.profile.group, self.group)
        self.assertEqual(self.profile.url, "http://example.com/profile")


class PostModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.post = Post.objects.create(
            title="Test Post",
            group=self.group,
            discovered=timezone.now(),
            published=timezone.now(),
            url="http://example.com/post",
            country="Test Country",
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.group, self.group)
        self.assertEqual(self.post.url, "http://example.com/post")
        self.assertEqual(self.post.country, "Test Country")
