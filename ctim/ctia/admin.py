# ctim/ctia/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.telegram import Channel, ChannelPost, FailedChannelPost
from ctim.ctia.models.threat_actor import CVE, Mitigation, RelatedThreatGroup, Risk, ThreatActor

admin.site.site_header = "Agentia Administration"
admin.site.site_title = "Agentia Administration Portal"
admin.site.index_title = "Welcome to Agentia - data editing and agent configuration."


@admin.register(ThreatActor)
class ThreatActorAdmin(ModelAdmin):
    list_display = ("name", "origin", "activity_period")  # Adjust fields as needed
    search_fields = ("name", "notable_info")
    list_filter = ("origin",)


@admin.register(Mitigation)
class MitigationAdmin(ModelAdmin):
    list_display = ("description", "threat_actor_display")
    list_filter = ("threat_actor",)
    search_fields = ("description", "threat_actor__name")

    @admin.display(description="Threat Actor")
    def threat_actor_display(self, obj):
        return obj.threat_actor.name


@admin.register(RelatedThreatGroup)
class RelatedThreatGroupAdmin(ModelAdmin):
    list_display = ("main_group_name", "related_group_name")
    list_filter = ("main_group", "related_group")
    search_fields = ("main_group__name", "related_group__name")

    @admin.display(description="Main Group")
    def main_group_name(self, obj):
        return obj.main_group.name

    @admin.display(description="Related Group")
    def related_group_name(self, obj):
        return obj.related_group.name


@admin.register(CVE)
class CVEAdmin(ModelAdmin):
    list_display = ("cve_id", "threat_actor_name", "description", "exploited_vulnerabilities")
    list_filter = ("threat_actor",)
    search_fields = ("cve_id", "description", "exploited_vulnerabilities", "threat_actor__name")

    @admin.display(description="Threat Actor")
    def threat_actor_name(self, obj):
        return obj.threat_actor.name


@admin.register(Risk)
class RiskAdmin(ModelAdmin):
    list_display = ("description", "threat_actor_display")
    list_filter = ("threat_actor",)
    search_fields = ("description", "threat_actor__name")

    @admin.display(description="Threat Actor")
    def threat_actor_display(self, obj):
        return obj.threat_actor.name


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title", "group", "discovered", "published", "country")
    search_fields = ("title", "group__name", "country")
    list_filter = ("group", "country", "published")


class PostInline(admin.TabularInline):
    model = Post
    extra = 1  # Number of empty forms to display


@admin.register(Location)
class LocationAdmin(ModelAdmin):
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
class ProfileAdmin(ModelAdmin):
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
class GroupAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    # inlines = [LocationInline, ProfileInline, PostInline]


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
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
class ChannelPostAdmin(ModelAdmin):
    list_display = ("message_id", "content", "date_posted", "channel")
    list_filter = ("date_posted", "channel")
    search_fields = ("content",)


@admin.register(FailedChannelPost)
class FailedChannelPostAdmin(ModelAdmin):
    list_display = ("channel_post_data", "error_message", "retry_count", "last_attempt_time")
    list_filter = ("retry_count", "last_attempt_time")
    search_fields = ("error_message",)
