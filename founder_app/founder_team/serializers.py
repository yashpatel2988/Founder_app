from rest_framework import serializers
from .models import FounderTeamsProfile

class TeamInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FounderTeamsProfile
        fields = ['id', 'daftar', 'name', 'designation', 'team_email', 'phone_number', 'invitation_token', 'is_active', 'created_date', 'last_updated_date']
        read_only_fields = ['invitation_token', 'is_active', 'created_date', 'last_updated_date']
