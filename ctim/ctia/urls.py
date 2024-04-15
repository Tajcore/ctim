from rest_framework.routers import DefaultRouter

from ctim.ctia.views import (
    CVEViewSet,
    GroupViewSet,
    LocationViewSet,
    MitigationViewSet,
    PostViewSet,
    ProfileViewSet,
    RelatedThreatGroupViewSet,
    RiskViewSet,
    ThreatActorViewSet,
)

router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)
router.register(r"threat-actors", ThreatActorViewSet)
router.register(r"mitigations", MitigationViewSet)
router.register(r"related-threat-groups", RelatedThreatGroupViewSet)
router.register(r"cves", CVEViewSet)
router.register(r"risks", RiskViewSet)


urlpatterns = router.urls
