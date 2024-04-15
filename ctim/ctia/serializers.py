from rest_framework import serializers

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.threat_actor import CVE, Mitigation, RelatedThreatGroup, Risk, ThreatActor


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]  # Only basic fields


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "description"]  # Include the description


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"  # Adjust fields as needed


class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mitigation
        fields = "__all__"


class RelatedThreatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedThreatGroup
        fields = "__all__"


class CVESerializer(serializers.ModelSerializer):
    class Meta:
        model = CVE
        fields = "__all__"


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = "__all__"


class ThreatActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatActor
        fields = "__all__"
