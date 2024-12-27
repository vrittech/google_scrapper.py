from rest_framework.routers import DefaultRouter
from ..viewsets.proxypool_viewsets import proxypoolViewsets
from ..viewsets.userproxyassignment_viewsets import userproxyassignmentViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('proxypool', proxypoolViewsets, basename="proxypoolViewsets")
router.register('userproxyassignment', userproxyassignmentViewsets, basename="userproxyassignmentViewsets")
