import logging

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView
from rest_framework import viewsets

from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.threat_actor import CVE, Mitigation, RelatedThreatGroup, Risk, ThreatActor
from ctim.ctia.serializers import (
    CVESerializer,
    GroupDetailSerializer,
    GroupListSerializer,
    LocationSerializer,
    MitigationSerializer,
    PostSerializer,
    ProfileSerializer,
    RelatedThreatGroupSerializer,
    RiskSerializer,
    ThreatActorSerializer,
)

logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Group.objects.all().order_by("name")
    filterset_fields = ["name"]

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update"] or "name" in self.request.query_params:
            return GroupDetailSerializer
        elif self.action == "list":
            return GroupListSerializer
        return super().get_serializer_class()


class LocationViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Location.objects.all().order_by("group", "fqdn", "available")
    serializer_class = LocationSerializer
    filterset_fields = ["group", "fqdn", "available"]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("group", "url")
    serializer_class = ProfileSerializer
    filterset_fields = ["group", "url"]


class CustomSchemaGenerator(SchemaGenerator):
    authentication_classes = []
    permission_classes = []

    def get_endpoints(self, request=None):
        endpoints = super().get_endpoints(request)
        # Filter out non-ctia endpoints
        ctia_endpoints = {path: path_info for path, path_info in endpoints.items() if path.startswith("/ctia/")}
        # Log the filtered endpoints at the debug level
        logger.debug(f"Filtered CTIA endpoints: {ctia_endpoints}")
        return ctia_endpoints


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Post.objects.all().order_by("-published")  # Order by 'published' in descending order
    serializer_class = PostSerializer
    filterset_fields = ["title", "group", "published"]


class CustomSchemaView(SpectacularAPIView):
    generator_class = CustomSchemaGenerator


class MitigationViewSet(viewsets.ModelViewSet):
    queryset = Mitigation.objects.all()
    serializer_class = MitigationSerializer
    filterset_fields = ["threat_actor"]


class RelatedThreatGroupViewSet(viewsets.ModelViewSet):
    queryset = RelatedThreatGroup.objects.all()
    serializer_class = RelatedThreatGroupSerializer
    filterset_fields = ["main_group", "related_group"]


class CVEViewSet(viewsets.ModelViewSet):
    queryset = CVE.objects.all()
    serializer_class = CVESerializer
    filterset_fields = ["threat_actor"]


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
    filterset_fields = ["threat_actor"]


class ThreatActorViewSet(viewsets.ModelViewSet):
    queryset = ThreatActor.objects.all()
    serializer_class = ThreatActorSerializer
    filterset_fields = ["name", "origin"]
