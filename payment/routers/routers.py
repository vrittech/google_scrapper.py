from rest_framework.routers import DefaultRouter
from ..viewsets.payment_viewsets import paymentViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('payment', paymentViewsets, basename="paymentViewsets")
