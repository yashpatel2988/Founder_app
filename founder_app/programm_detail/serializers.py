from rest_framework import serializers
from .models import InvesterPrograms

class InvesterProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvesterPrograms
        fields = ['id', 'elevator_pitch', 'title', 'collabration', 'collabration_url', 'team', 'sector', 'capital', 'equity', 'stage', 'last_date_of_pitch', 'community', 'location', 'age_group', 'gender', 'view', 'shared', 'last_updated_date', 'last_updated_by', 'created_date', 'created_by', 'invester']
