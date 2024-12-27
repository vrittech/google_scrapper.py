from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SubscriptionPlan
from ..serializers.subscriptionplan_serializers import SubscriptionPlanListSerializers, SubscriptionPlanRetrieveSerializers, SubscriptionPlanWriteSerializers
from ..utilities.importbase import *

class subscriptionplanViewsets(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanListSerializers
    # permission_classes = [subscriptionplanPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = SubscriptionPlan.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SubscriptionPlanWriteSerializers
        elif self.action == 'retrieve':
            return SubscriptionPlanRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

