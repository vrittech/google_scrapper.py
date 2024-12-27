from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProxyPool
from ..serializers.proxypool_serializers import ProxyPoolListSerializers, ProxyPoolRetrieveSerializers, ProxyPoolWriteSerializers
from ..utilities.importbase import *

class proxypoolViewsets(viewsets.ModelViewSet):
    serializer_class = ProxyPoolListSerializers
    # permission_classes = [proxypoolPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = ProxyPool.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProxyPoolWriteSerializers
        elif self.action == 'retrieve':
            return ProxyPoolRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

