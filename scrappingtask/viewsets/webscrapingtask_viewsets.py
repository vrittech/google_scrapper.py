from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import WebScrapingTask
from ..serializers.webscrapingtask_serializers import WebScrapingTaskListSerializers, WebScrapingTaskRetrieveSerializers, WebScrapingTaskWriteSerializers
from ..utilities.importbase import *

class webscrapingtaskViewsets(viewsets.ModelViewSet):
    serializer_class = WebScrapingTaskListSerializers
    # permission_classes = [scrappingtaskPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = WebScrapingTask.objects.all().order_by('-id')

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
            return WebScrapingTaskWriteSerializers
        elif self.action == 'retrieve':
            return WebScrapingTaskRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

