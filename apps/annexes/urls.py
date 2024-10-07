from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, ApplicationViewSet, BuildingViewSet, DriverViewSet, CategoryAPIViews, ReviewAPIViews

router = DefaultRouter()
router.register("certificates", CertificateViewSet)
router.register("applications", ApplicationViewSet)
router.register("buildings", BuildingViewSet)
router.register("drivers", DriverViewSet)
router.register("category", CategoryAPIViews)
router.register("review", ReviewAPIViews)

urlpatterns = router.urls