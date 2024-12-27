from rest_framework.routers import DefaultRouter
from ..viewsets.webscrapingtask_viewsets import webscrapingtaskViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('webscrapingtask', webscrapingtaskViewsets, basename="webscrapingtaskViewsets")
