"""
URL configuration for personal_prot_tracker_inv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.urls import include, path, re_path
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.views.generic.base import RedirectView

# Schema view for DRF-YASG
schema_view = get_schema_view(
   openapi.Info(
      title="Personal Portfolio Tracker API",
      default_version='v1',
      description="API for managing user portfolios, watchlists, and stock analysis.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="amar@tracker.com"), # Replace with your email
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# from app import app_urls

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
     # NEW: Add this line to redirect the root URL to the Swagger docs
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),

    path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path('api/', include('app.app_urls')),  # Include the app's URLs
    # DRF-YASG URLs for API documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

# Add this line to include your portfolio app's URLs
    # All URLs from the portfolio app will now be prefixed with 'api/portfolio/'
    path('api/portfolio/', include('portfolio.urls')),
    
    

]
