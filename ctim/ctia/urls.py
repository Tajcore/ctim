from rest_framework.routers import DefaultRouter

from ctim.ctia.views import GroupViewSet, LocationViewSet, PostViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)

urlpatterns = router.urls
