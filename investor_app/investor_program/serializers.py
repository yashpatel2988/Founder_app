from rest_framework import serializers
from .models import InvesterPrograms

class InvesterProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvesterPrograms
        fields = '__all__'
