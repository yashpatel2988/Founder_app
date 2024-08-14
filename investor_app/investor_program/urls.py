from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PitchVideoViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'investor_program', PitchVideoViewSet, basename='investor_program')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
