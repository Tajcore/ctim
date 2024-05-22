# ctim/ctim/ctia/serializers.py

from rest_framework import serializers

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.threat_actor import CVE, Mitigation, RelatedThreatGroup, Risk, ThreatActor


class CaseInsensitiveGroupNameField(serializers.CharField):
    def to_internal_value(self, data):
        # Explicit validation: Ensure that the input data is a non-empty string
        if not isinstance(data, str) or not data.strip():
            raise serializers.ValidationError("Group name must be a non-empty string.")

        # Transform the input data into an internal representation
        return self.get_group_by_name(data)

    def get_group_by_name(self, name):
        # Retrieve the group object with case-insensitive matching
        return Group.objects.filter(name__iexact=name).first()


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]  # Only basic fields


class GroupDetailSerializer(serializers.ModelSerializer):
    name = CaseInsensitiveGroupNameField()

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
