from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ScrapedData
from ..serializers.scrapeddata_serializers import ScrapedDataListSerializers, ScrapedDataRetrieveSerializers, ScrapedDataWriteSerializers
from ..utilities.importbase import *

class scrapeddataViewsets(viewsets.ModelViewSet):
    serializer_class = ScrapedDataListSerializers
    # permission_classes = [scrapingPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ScrapedData.objects.all()

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
            return ScrapedDataWriteSerializers
        elif self.action == 'retrieve':
            return ScrapedDataRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

