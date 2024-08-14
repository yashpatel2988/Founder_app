# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DaftarViewSet, CreatePitchViewSet, PitchVideoViewSet,DaftarDetailViewSet

router = DefaultRouter()
router.register(r'daftar', DaftarViewSet)
router.register(r'create_pitch', CreatePitchViewSet)
router.register(r'pitch_video', PitchVideoViewSet)
router.register(r'daftar_detail', DaftarDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
