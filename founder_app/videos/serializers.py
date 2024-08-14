# serializers.py

from rest_framework import serializers
from .models import FounderDaftar, CreatePitch, PitchVideos,DaftarDetail
from rest_framework import serializers
from .models import FounderDaftar

class DaftarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FounderDaftar
        fields = '__all__'

    def validate(self, data):
        founder = data.get('founder')
        daftar_name = data.get('daftar_name')

        # Check if the combination of user and daftar_name already exists
        if FounderDaftar.objects.filter(founder=founder, daftar_name=daftar_name).exists():
            raise serializers.ValidationError({
                'non_field_errors': [
                    'A FounderDaftar with this user and name already exists.'
                ]
            })
        
        return data


class CreatePitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatePitch
        fields = '__all__'

class PitchVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchVideos
        fields = '__all__'
        #fields = ['id','user','daftar','pitch', 'question_id', 'question_language', 'question_url', 'last_updated_date', 'updated_by', 'created_date', 'created_by']

class DaftarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaftarDetail
        fields = '__all__'