from rest_framework.routers import DefaultRouter
from ..viewsets.apilog_viewsets import apilogViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('apilog', apilogViewsets, basename="apilogViewsets")
