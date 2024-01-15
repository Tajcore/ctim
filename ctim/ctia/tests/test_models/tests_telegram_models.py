# ctim/ctia/tests/test_models/tests_telegram_models.py
from django.test import TestCase
from django.utils import timezone

from ctim.ctia.models.telegram import Adjacency, Channel, ChannelPost, Media, Message, UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            user_id=12345,
            bio="Test bio",
            online_status="Online",
            # Add a mock image file for profile_picture if needed
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.username, "testuser")
        self.assertEqual(self.user_profile.first_name, "Test")
        self.assertEqual(self.user_profile.last_name, "User")
        self.assertEqual(self.user_profile.phone_number, "1234567890")
        self.assertEqual(self.user_profile.user_id, 12345)
        self.assertEqual(self.user_profile.bio, "Test bio")
        self.assertEqual(self.user_profile.online_status, "Online")
        # Test for profile_picture if applicable


class ChannelModelTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(username="testuser", user_id=12345)
        self.channel = Channel.objects.create(
            name="Test Channel",
            description="Test Description",
            url="http://example.com/channel",
            source_urls="http://source1.com, http://source2.com"
            # Add data for metadata if needed
        )
        self.channel.members.add(self.user_profile)

    def test_channel_creation(self):
        self.assertEqual(self.channel.name, "Test Channel")
        self.assertEqual(self.channel.description, "Test Description")
        self.assertEqual(self.channel.url, "http://example.com/channel")
        self.assertIn(self.user_profile, self.channel.members.all())
        self.assertEqual(self.channel.source_urls, "http://source1.com, http://source2.com")
        # Test for metadata if applicable


class AdjacencyModelTest(TestCase):
    def setUp(self):
        self.source_channel = Channel.objects.create(name="Source Channel")
        self.target_channel = Channel.objects.create(name="Target Channel")
        self.adjacency = Adjacency.objects.create(
            source_channel=self.source_channel, target_channel=self.target_channel
        )

    def test_adjacency_creation(self):
        self.assertEqual(self.adjacency.source_channel, self.source_channel)
        self.assertEqual(self.adjacency.target_channel, self.target_channel)
        # Test the weight property if applicable


class MessageModelTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(username="testuser", user_id=12345)
        self.channel = Channel.objects.create(name="Test Channel")
        self.message = Message.objects.create(
            content="Test Content",
            date_posted=timezone.now(),
            user=self.user_profile,
            channel=self.channel,
            views=100,
            message_url="http://example.com/message",
        )

    def test_message_creation(self):
        self.assertEqual(self.message.content, "Test Content")
        self.assertIsNotNone(self.message.date_posted)
        self.assertEqual(self.message.user, self.user_profile)
        self.assertEqual(self.message.channel, self.channel)
        self.assertEqual(self.message.views, 100)
        self.assertEqual(self.message.message_url, "http://example.com/message")


class MediaModelTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(username="testuser", user_id=12345)
        self.channel = Channel.objects.create(name="Test Channel")
        self.message = Message.objects.create(
            content="Test Content", user=self.user_profile, channel=self.channel, date_posted=timezone.now()
        )
        self.media = Media.objects.create(
            message=self.message
            # Add a mock file for media_file if needed
        )

    def test_media_creation(self):
        self.assertEqual(self.media.message, self.message)
        # Test for media_file if applicable


class ChannelPostModelTest(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(
            name="Test Channel",
            description="A test channel",
            url="http://example.com/channel",
            source_urls="http://source1.com, http://source2.com",
        )
        self.channel_post = ChannelPost.objects.create(
            channel=self.channel,
            message_id=123456789,
            content="Test Post Content",
            date_posted=timezone.now(),
            views=100,
            forwards=10,
            reply_count=5,
            media_json={"type": "photo", "url": "http://example.com/photo.jpg"},
            entities_json=[{"type": "url", "offset": 10, "length": 20}],
            message_url="http://example.com/post/123456789",
        )

    def test_channel_post_creation(self):
        self.assertEqual(self.channel_post.channel, self.channel)
        self.assertEqual(self.channel_post.message_id, 123456789)
        self.assertEqual(self.channel_post.content, "Test Post Content")
        self.assertIsNotNone(self.channel_post.date_posted)
        self.assertEqual(self.channel_post.views, 100)
        self.assertEqual(self.channel_post.forwards, 10)
        self.assertEqual(self.channel_post.reply_count, 5)
        self.assertEqual(self.channel_post.media_json, {"type": "photo", "url": "http://example.com/photo.jpg"})
        self.assertEqual(self.channel_post.entities_json, [{"type": "url", "offset": 10, "length": 20}])
        self.assertEqual(self.channel_post.message_url, "http://example.com/post/123456789")
