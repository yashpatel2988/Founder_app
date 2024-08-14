import os
import re
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import FounderDaftar, CreatePitch, PitchVideos, DaftarDetail, FounderProfile
from .serializers import DaftarSerializer, CreatePitchSerializer, PitchVideoSerializer, DaftarDetailSerializer
from .compress import convert_video
from django.db import IntegrityError

class DaftarViewSet(viewsets.ModelViewSet):
    queryset = FounderDaftar.objects.all()
    serializer_class = DaftarSerializer

    @action(detail=False, methods=['post'])
    def create_daftar(self, request):
        data = request.data
        founder_id = data.get('founder')
        daftar_name = data.get('daftar_name')

        if not founder_id or not daftar_name:
            return Response(
                {'error': 'founder and daftar_name are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if FounderDaftar.objects.filter(founder_id_id=founder_id, daftar_name=daftar_name).exists():
            return Response(
                {'message': 'A Daftar with this user and name already exists.'},
                status=status.HTTP_200_OK
            )

        serializer = DaftarSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': 'An error occurred while creating the Daftar entry.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_by_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        daftars = FounderDaftar.objects.filter(created_by=user_id)
        serializer = DaftarSerializer(daftars, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='update_daftar')
    def update_daftar(self, request):
        daftar_id = request.query_params.get('daftar_id')
        if not daftar_id:
            return Response({"error": "daftar_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            daftar_id = int(re.sub(r'\D', '', daftar_id))
        except ValueError:
            return Response({"error": "daftar_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        daftar_instance = get_object_or_404(FounderDaftar, pk=daftar_id)

        serializer = DaftarSerializer(daftar_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete_daftar')
    def delete_daftar(self, request):
        daftar_id = request.query_params.get('daftar_id')
        if not daftar_id:
            return Response({"error": "daftar_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            daftar_id = int(re.sub(r'\D', '', daftar_id))
        except ValueError:
            return Response({"error": "daftar_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        daftar_instance = get_object_or_404(FounderDaftar, pk=daftar_id)
        daftar_instance.is_active = False
        daftar_instance.save()

        return Response({"message": "Daftar marked as deleted successfully."}, status=status.HTTP_200_OK)


class CreatePitchViewSet(viewsets.ModelViewSet):
    queryset = CreatePitch.objects.all()
    serializer_class = CreatePitchSerializer

    @action(detail=False, methods=['get'], url_path='pitch_detail')
    def get_daftar_details(self, request, *args, **kwargs):
        daftar_id = request.query_params.get('daftar_id')
        if not daftar_id:
            return Response({'error': 'daftar_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        daftar_details = CreatePitch.objects.filter(daftar_id=daftar_id)
        serializer = CreatePitchSerializer(daftar_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class PitchVideoViewSet(viewsets.ModelViewSet):
    queryset = PitchVideos.objects.all()
    serializer_class = PitchVideoSerializer

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_media(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        daftar_id = request.data.get('daftar_id')
        pitch_id = request.data.get('pitch_id')
        question_id = request.data.get('question_id')
        question_language = request.data.get('question_language')
        last_updated_by = request.data.get('last_updated_by')
        created_by = request.data.get('created_by')

        if not all([user_id, daftar_id, pitch_id, question_id, question_language]):
            return Response({'error': 'All required fields must be provided'}, status=400)

        try:
            user_profile = FounderProfile.objects.get(id=user_id)
        except FounderProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File is required'}, status=400)

        file_type = file.content_type.split('/')[0]
        file_name = file.name

        base_folder = os.path.join('media_files', f'USER{user_id}', f'DOS{daftar_id}', f'PITCH{pitch_id}', f'QUE{question_id}')
        media_folder = os.path.join(base_folder, file_type)

        os.makedirs(media_folder, exist_ok=True)
        file_path = os.path.join(media_folder, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            if file_type == 'video':
                converted_data = convert_video(file_path, size=5)
            else:
                # Handle audio or other media types if needed
                converted_data = file.read()

            final_file_path = os.path.join(media_folder, file_name)
            with open(final_file_path, 'wb') as f:
                f.write(converted_data)

            pitch_video = PitchVideos(
                founder=user_profile,
                pitch_id=pitch_id,
                question_id=question_id,
                question_language=question_language,
                question_url=final_file_path,
                last_updated_by=last_updated_by,
                created_by=created_by
            )
            pitch_video.save()

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        serializer = PitchVideoSerializer(pitch_video)
        return Response({'message': 'File uploaded and processed successfully', 'pitch_video': serializer.data}, status=200)


class DaftarDetailViewSet(viewsets.ModelViewSet):
    queryset = DaftarDetail.objects.all()
    serializer_class = DaftarDetailSerializer

    @action(detail=False, methods=['post'], url_path='create_daftar_detail')
    def create_daftar_detail(self, request, *args, **kwargs):
        serializer = DaftarDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='get_daftar_details')
    def get_daftar_details(self, request, *args, **kwargs):
        daftar_id = request.query_params.get('daftar_id')
        if not daftar_id:
            return Response({'error': 'daftar_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        daftar_details = DaftarDetail.objects.filter(daftar_id=daftar_id)
        serializer = DaftarDetailSerializer(daftar_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
