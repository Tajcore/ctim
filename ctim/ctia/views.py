import logging

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView
from rest_framework import viewsets

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.serializers import (
    GroupDetailSerializer,
    GroupListSerializer,
    LocationSerializer,
    PostSerializer,
    ProfileSerializer,
)

logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    filterset_fields = ["name"]

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update"] or "name" in self.request.query_params:
            return GroupDetailSerializer
        elif self.action == "list":
            return GroupListSerializer
        return super().get_serializer_class()


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("group", "fqdn", "available")
    serializer_class = LocationSerializer
    filterset_fields = ["group", "fqdn", "available"]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("group", "url")
    serializer_class = ProfileSerializer
    filterset_fields = ["group", "url"]


class CustomSchemaGenerator(SchemaGenerator):
    def get_endpoints(self, request=None):
        endpoints = super().get_endpoints(request)
        # Filter out non-ctia endpoints
        ctia_endpoints = {path: path_info for path, path_info in endpoints.items() if path.startswith("/ctia/")}
        # Log the filtered endpoints at the debug level
        logger.debug(f"Filtered CTIA endpoints: {ctia_endpoints}")
        return ctia_endpoints


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published")  # Order by 'published' in descending order
    serializer_class = PostSerializer
    filterset_fields = ["title", "group", "published"]


class CustomSchemaView(SpectacularAPIView):
    generator_class = CustomSchemaGenerator
