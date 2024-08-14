from rest_framework import serializers
from .models import InvesterProfile
from datetime import datetime

class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = InvesterProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'age']

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.today()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None
