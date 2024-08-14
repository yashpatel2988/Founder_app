from django.urls import path
from .views import UserProfileViewSet, UserDetailView, UserRegistrationView


urlpatterns = [
    path('user_detail/', UserDetailView.as_view(), name='user-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('update_profile/', UserProfileViewSet.as_view({'put': 'update_profile'}), name='profile-update'),
    path('soft_delete/', UserProfileViewSet.as_view({'delete': 'soft_delete'}), name='profile-soft-delete'),
]
