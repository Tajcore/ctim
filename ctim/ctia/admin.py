# ctim/ctia/admin.py
from django.contrib import admin

from ctim.ctia.models.ransomware import Group, Location, Post, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "discovered", "published", "country")
    search_fields = ("title", "group__name", "country")
    list_filter = ("group", "country", "published")


class PostInline(admin.TabularInline):
    model = Post
    extra = 1  # Number of empty forms to display


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "fqdn",
        "title",
        "version",
        "slug",
        "available",
        "delay",
        "updated",
        "lastscrape",
        "enabled",
    )
    list_filter = ("group", "available", "enabled")
    search_fields = ("fqdn", "title")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("group", "url")
    list_filter = ("group",)
    search_fields = ("url",)


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1  # Number of empty forms to display


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "captcha", "parser", "javascript_render", "description")
    search_fields = ("name",)
    inlines = [LocationInline, ProfileInline, PostInline]


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1
