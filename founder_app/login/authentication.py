# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthenticationCustom(JWTAuthentication):
    def authenticate(self, request):
        jwt_auth = super().authenticate(request)
        if jwt_auth is not None:
            user, _ = jwt_auth
            return (user, jwt_auth[1])
        return None
