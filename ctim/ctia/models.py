# ctim/ctia/models.py
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    captcha = models.BooleanField(default=False)
    parser = models.BooleanField(default=False)
    javascript_render = models.BooleanField(default=False)
    meta = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Location(models.Model):
    group = models.ForeignKey(Group, related_name="locations", on_delete=models.CASCADE)
    fqdn = models.CharField(max_length=1000)
    title = models.CharField(max_length=100, null=True)
    version = models.IntegerField()
    slug = models.URLField()
    available = models.BooleanField()
    delay = models.FloatField(null=True, blank=True)
    updated = models.DateTimeField()
    lastscrape = models.DateTimeField()
    enabled = models.BooleanField()


class Profile(models.Model):
    group = models.ForeignKey(Group, related_name="profiles", on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)
