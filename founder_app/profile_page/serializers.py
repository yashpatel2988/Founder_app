from rest_framework import serializers
from .models import FounderProfile
from datetime import datetime

class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = FounderProfile
        fields = '__all__'  # Include all fields in the response

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.today()
            age = today.year - obj.date_of_birth.year
            if today.month < obj.date_of_birth.month or (today.month == obj.date_of_birth.month and today.day < obj.date_of_birth.day):
                age -= 1
            return age
        return None