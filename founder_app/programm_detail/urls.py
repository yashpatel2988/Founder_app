from django.urls import path
from .views import InvesterProgramsViewSet

urlpatterns = [
    # Endpoint to fetch all programs
    path('programs_list/', InvesterProgramsViewSet.as_view({'get': 'list'}), name='programs-list'),
    # Endpoint to fetch video for a specific program
    path('<int:pk>/video/', InvesterProgramsViewSet.as_view({'get': 'get_video'}), name='program-video'),
    # Endpoint to get programs by pitch ID
    path('programs_list/pitch_programs/', InvesterProgramsViewSet.as_view({'get': 'get_pitch_programs'}), name='pitch-programs'),
]
