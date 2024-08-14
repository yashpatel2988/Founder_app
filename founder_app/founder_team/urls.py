from django.urls import path
from .views import TeamInviteView, AcceptInviteView

urlpatterns = [
    path('invite/', TeamInviteView.as_view(), name='team-invite'),
    path('accept/<str:token>/', AcceptInviteView.as_view(), name='accept-invite'),
]
