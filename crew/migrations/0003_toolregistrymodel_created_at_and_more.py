# Generated by Django 4.2.8 on 2024-06-05 09:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("crew", "0002_toolregistrymodel_toolmodel_agentmodel_tools_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="toolregistrymodel",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="toolregistrymodel",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
