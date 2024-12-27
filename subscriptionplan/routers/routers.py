from rest_framework.routers import DefaultRouter
from ..viewsets.subscriptionplan_viewsets import subscriptionplanViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('subscriptionplan', subscriptionplanViewsets, basename="subscriptionplanViewsets")
