from django.urls import path
from .views import google_sign_in, refresh_token

urlpatterns = [
    path('google_sign_in/', google_sign_in, name='google_sign_in'),
    path('refresh-token/', refresh_token, name='refresh_token'),
]
