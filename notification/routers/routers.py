from rest_framework.routers import DefaultRouter
from ..viewsets.notification_viewsets import notificationViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('notification', notificationViewsets, basename="notificationViewsets")
