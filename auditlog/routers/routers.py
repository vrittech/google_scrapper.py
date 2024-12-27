from rest_framework.routers import DefaultRouter
from ..viewsets.auditlog_viewsets import auditlogViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('auditlog', auditlogViewsets, basename="auditlogViewsets")
