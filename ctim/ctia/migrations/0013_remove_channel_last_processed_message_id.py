# Generated by Django 4.2.8 on 2024-01-09 09:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ctia", "0012_alter_channel_members_alter_channel_source_urls"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="channel",
            name="last_processed_message_id",
        ),
    ]