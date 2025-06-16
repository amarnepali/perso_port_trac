from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserIndexViewSet, UserProfileViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'userindex', UserIndexViewSet, basename='userindex')
router.register(r'userprofile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    # path('', include(router.urls)),
    path('userindex/', UserIndexViewSet.as_view()),
    # You can add more paths here if needed
]


