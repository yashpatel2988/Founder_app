from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import os

from .models import InvesterPrograms, Sector, Community
from .serializers import InvesterProgramsSerializer
from .compress import convert_video  # Assuming you have a utility function for video conversion

class PitchVideoViewSet(viewsets.ModelViewSet):
    queryset = InvesterPrograms.objects.all()
    serializer_class = InvesterProgramsSerializer

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_media(self, request, *args, **kwargs):
        try:
            # Retrieve necessary data from the request
            elevator_pitch = request.data.get('elevator_pitch')
            title = request.data.get('title')
            collabration = request.data.get('collabration')
            collabration_url = request.data.get('collabration_url')
            team = request.data.get('team')
            sector_id = request.data.get('sector')
            capital = request.data.get('capital')
            equity = request.data.get('equity')
            stage = request.data.get('stage')
            last_date_of_pitch = request.data.get('last_date_of_pitch')
            community_id = request.data.get('community')
            location = request.data.get('location')
            age_group = request.data.get('age_group')
            gender = request.data.get('gender')
            view = request.data.get('view')
            shared = request.data.get('shared')
            last_updated_by = request.data.get('last_updated_by')
            created_by = request.data.get('created_by')
            invester = request.data.get('invester')

            # Check if required fields are missing
            required_fields = [elevator_pitch, title, collabration, collabration_url, team, sector_id, capital, equity, stage, last_date_of_pitch, community_id, location]
            if not all(required_fields):
                return Response({'error': 'All required fields are not provided'}, status=400)

            # Fetch related instances
            try:
                sector = Sector.objects.get(id=sector_id)
                community = Community.objects.get(id=community_id)
            except (Sector.DoesNotExist, Community.DoesNotExist) as e:
                return Response({'error': str(e)}, status=404)

            # Prepare for file upload
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'File is required'}, status=400)

            file_type = file.content_type.split('/')[0]
            file_name = file.name

            # Define file paths for storing the uploaded media
            base_folder = os.path.join('media_files', f'TEAM{team}', f'SECTOR{sector_id}', f'PITCH{elevator_pitch}', f'QUE{last_date_of_pitch}')
            video_folder = os.path.join(base_folder, 'video')

            os.makedirs(video_folder, exist_ok=True)

            file_path = os.path.join(video_folder, file_name)

            # Save the uploaded file to the specified path
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Process and save the uploaded file based on its type
            if file_type == 'video':
                try:
                    converted_data = convert_video(file_path, size=5)  # Convert the video file
                    final_file_path = os.path.join(video_folder, file_name)

                    with open(final_file_path, 'wb') as f:
                        f.write(converted_data)
                except Exception as e:
                    return Response({'error': f'Error processing video: {str(e)}'}, status=500)
            else:
                return Response({'error': 'Unsupported file type'}, status=400)

            # Create or update an InvesterPrograms entry
            invester_program = InvesterPrograms.objects.update_or_create(
                id=request.data.get('id'),  # Use ID from request to update or create
                defaults={
                    'elevator_pitch': elevator_pitch,
                    'title': title,
                    'collabration': collabration,
                    'collabration_url': collabration_url,
                    'team': team,
                    'sector': sector,
                    'capital': capital,
                    'equity': equity,
                    'stage': stage,
                    'last_date_of_pitch': last_date_of_pitch,
                    'community': community,
                    'location': location,
                    'age_group': age_group,
                    'gender': gender,
                    'view': view,
                    'shared': shared,
                    'last_updated_by': last_updated_by,
                    'created_by': created_by,
                    'invester': invester
                }
            )

            serializer = InvesterProgramsSerializer(invester_program)
            return Response({'message': 'File uploaded and processed successfully', 'pitch_video': serializer.data}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
