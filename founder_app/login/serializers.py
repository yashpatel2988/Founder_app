# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id  # Use `user.id` for the primary key
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.login_id  # Use `login_id` for the email

        return token
