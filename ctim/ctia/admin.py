# ctim/ctia/admin.py
from django.contrib import admin

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.telegram import Channel, ChannelPost, FailedChannelPost


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
    list_display = ("name", "description")
    search_fields = ("name",)
    # inlines = [LocationInline, ProfileInline, PostInline]


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "description", "display_last_processed_message_id")
    search_fields = (
        "name",
        "url",
    )
    fields = ("name", "url", "description", "is_being_processed")  # Corrected field name

    # Optional: If you want to display the value of last_processed_message_id in the admin change view
    readonly_fields = ("display_last_processed_message_id",)

    @admin.display(description="Last Processed Message ID")
    def display_last_processed_message_id(self, obj):
        return obj.last_processed_message_id


@admin.register(ChannelPost)
class ChannelPostAdmin(admin.ModelAdmin):
    list_display = ("message_id", "content", "date_posted", "channel")
    list_filter = ("date_posted", "channel")
    search_fields = ("content",)


@admin.register(FailedChannelPost)
class FailedChannelPostAdmin(admin.ModelAdmin):
    list_display = ("channel_post_data", "error_message", "retry_count", "last_attempt_time")
    list_filter = ("retry_count", "last_attempt_time")
    search_fields = ("error_message",)
