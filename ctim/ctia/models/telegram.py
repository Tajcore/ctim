# ctim/ctia/models/telegram.py
import json  # For storing JSON data

from django.db import connection, models
from django.db.models import JSONField


class UserProfile(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    user_id = models.BigIntegerField()
    bio = models.TextField(null=True, blank=True)
    online_status = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)


class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    members = models.ManyToManyField(UserProfile, related_name="channels")
    source_urls = models.TextField(help_text="Comma-separated list of source URLs")
    metadata = JSONField(blank=True, null=True)  # Flexible storage for additional channel attributes

    def __str__(self):
        return self.name


class ChannelPost(models.Model):
    channel = models.ForeignKey(Channel, related_name="posts", on_delete=models.CASCADE)  # Link to Channel model
    message_id = models.BigIntegerField(unique=True)  # Unique ID of the message in the channel
    content = models.TextField()
    date_posted = models.DateTimeField()
    edit_date = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    forwards = models.IntegerField(null=True, blank=True)
    reply_count = models.IntegerField(default=0)
    media_json = models.JSONField(null=True, blank=True)  # Store media information as JSON
    entities_json = models.JSONField(null=True, blank=True)  # Store entities as JSON
    message_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Channel Post {self.message_id} in Channel {self.channel_id}"

    @property
    def entities(self):
        return json.loads(self.entities_json) if self.entities_json else None

    @property
    def media(self):
        return json.loads(self.media_json) if self.media_json else None


class Adjacency(models.Model):
    source_channel = models.ForeignKey(Channel, related_name="forwarded_from", on_delete=models.CASCADE)
    target_channel = models.ForeignKey(Channel, related_name="forwarded_to", on_delete=models.CASCADE)

    @property
    def weight(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM app_adjacency WHERE source_channel_id = %s AND target_channel_id = %s",
                [self.source_channel_id, self.target_channel_id],
            )
            row = cursor.fetchone()
        return row[0] if row else 0

    def __str__(self):
        return f"{self.source_channel.name} -> {self.target_channel.name} (Weight: {self.weight})"


class Message(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name="messages", on_delete=models.CASCADE)
    views = models.IntegerField(null=True, blank=True)
    message_url = models.URLField()

    def __str__(self):
        return f"Message by {self.user.username} on {self.date_posted}"


class Media(models.Model):
    message = models.ForeignKey(Message, related_name="media", on_delete=models.CASCADE)
    media_file = models.FileField(upload_to="message_media/")

    def __str__(self):
        return f"Message by {self.user.username} on {self.date_posted}"
