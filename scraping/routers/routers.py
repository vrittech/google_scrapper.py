from rest_framework.routers import DefaultRouter
from ..viewsets.scrapeddata_viewsets import scrapeddataViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('scrapeddata', scrapeddataViewsets, basename="scrapeddataViewsets")
