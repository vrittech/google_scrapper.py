from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from scraping.googlemapview import GoogleMapScrapingAPI
# from scraping.webscrapeview import WebsiteContactScrapingAPI
from scrappingtask.views import WebsiteContactScrapingAPI
from scraping.scraping import scrape_view, scrape_form
from  rest_framework  import routers

from accounts.urls import router as accounts_router
from apilog.routers.routers import router as apilog_router
from payment.routers.routers import router as payment_router
from scraping.routers.routers import router as scraping_router
from scrappingtask.routers.routers import router as scrappingtask_router
from subscriptionplan.routers.routers import router as subscriptionplan_router
from notification.routers.routers import router as notification_router
from auditlog.routers.routers import router as auditlog_router
from proxypool.routers.routers import router as proxypool_router

router = routers.DefaultRouter()

router.registry.extend(accounts_router.registry)
router.registry.extend(apilog_router.registry)
router.registry.extend(payment_router.registry)
router.registry.extend(scraping_router.registry)
router.registry.extend(scrappingtask_router.registry)
router.registry.extend(subscriptionplan_router.registry)
router.registry.extend(notification_router.registry)
router.registry.extend(auditlog_router.registry)
router.registry.extend(proxypool_router.registry)

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Web Scraping API",
        default_version='v1',
        description="Web Scraping API",
        terms_of_service="https://swagger.io/resources/open-api/",
        contact=openapi.Contact(email="prashantkarna21@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Default to Swagger UI
    path('admin/', admin.site.urls),
    path('api/google-map-scraping/', GoogleMapScrapingAPI.as_view(), name='google-map-scraping'),
    path('api/website-contact-scraping/', WebsiteContactScrapingAPI.as_view(), name='website-contact-scraping'),
    path('api/scrape/', scrape_view, name='scrape-view'),
    path('form/', scrape_form, name='scrape-form'),
    path('api-auth/', include('rest_framework.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/',include(router.urls)),
    path('api/accounts/',include('accounts.urls')),
    path('api/',include('accountsmanagement.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)