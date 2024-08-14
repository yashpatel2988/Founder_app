import requests
import uuid
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import FounderProfile
import jwt
import datetime

def verify_google_token(id_token):
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
    if response.status_code == 200:
        token_info = response.json()
        if token_info['aud'] == settings.GOOGLE_CLIENT_ID:
            return token_info
    return None

def get_or_create_user_profile(user_data):
    profile, created = FounderProfile.objects.get_or_create(
        login_id=user_data['email'],  # Use the email (login_id) as the unique identifier
        defaults={
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
        }
    )
    return profile

def generate_jwt(user_data):
    payload = {
        'user_id': user_data['user_id'],
        'login_id': user_data['login_id'],
        'exp': datetime.datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
    }
    print("JWT Secret Key:", settings.JWT_SECRET_KEY)  # Debug statement
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token():
    return str(uuid.uuid4())

@api_view(['POST'])
def google_sign_in(request):
    id_token = request.data.get('id_token')
    if not id_token:
        return JsonResponse({'error': 'No ID token provided'}, status=400)

    user_data = verify_google_token(id_token)
    if user_data:
        user_profile = get_or_create_user_profile(user_data)
        jwt_token = generate_jwt({'user_id': user_profile.user_id, 'login_id': user_profile.login_id})
        refresh_token = generate_refresh_token()
        user_profile.refresh_token = refresh_token
        user_profile.save()

        return JsonResponse({'token': jwt_token, 'refresh_token': refresh_token}, status=200)
    else:
        return JsonResponse({'error': 'Invalid ID token'}, status=400)

@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return JsonResponse({'error': 'No refresh token provided'}, status=400)

    try:
        user_profile = FounderProfile.objects.get(refresh_token=refresh_token)
    except FounderProfile.DoesNotExist:
        return JsonResponse({'error': 'Invalid refresh token'}, status=400)

    jwt_token = generate_jwt({'user_id': user_profile.user_id, 'login_id': user_profile.login_id})

    # Optionally rotate refresh token
    new_refresh_token = generate_refresh_token()
    user_profile.refresh_token = new_refresh_token
    user_profile.save()

    return JsonResponse({'token': jwt_token, 'refresh_token': new_refresh_token}, status=200)
