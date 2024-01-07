from rest_framework import serializers

from ctim.ctia.models.ransomware import Group, Location, Post, Profile


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
