from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, LocationViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = router.urls
