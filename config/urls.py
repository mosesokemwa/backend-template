"""university URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

API_PREFIX = f"api/{config('API_VERSION_PREFIX', default='v1')}"

public_apis = [
    path(f'{API_PREFIX}/auth/', include('apps.auth_app.urls')),
    path(f'{API_PREFIX}/', include('apps.health.urls')),
]


schema_view = get_schema_view(
    openapi.Info(
        title=config("API_TITLE"),
        default_version=config("API_VERSION"),
        description="These are the main APIs for Metro",
        terms_of_service=config("TOS_URL"),
        x_logo={
            "url": config("LOGO_URL"),
            "backgroundColor": "#FFFFFF"
        }
    ),
    public=True,
    patterns=public_apis,
    permission_classes=[permissions.AllowAny],
)
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('developer/docs', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('developer/doc', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
    path('favicon.ico', favicon_view),

    # enable the admin interface
    path('admin/', admin.site.urls),

]

urlpatterns += public_apis
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = config('ADMIN_SITE_HEADER')
admin.site.site_title = config('ADMIN_SITE_TITLE')
admin.site.index_title = config('ADMIN_SITE_INDEX_TITLE')
