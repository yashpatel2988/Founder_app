from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, FileResponse 
from .models import InvesterPrograms
from videos.models import CreatePitch
from .serializers import InvesterProgramsSerializer
import os
from django.shortcuts import get_object_or_404

class InvesterProgramsViewSet(viewsets.ViewSet):
    # Existing list method
    def list(self, request):
        queryset = InvesterPrograms.objects.all()
        serializer = InvesterProgramsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='video')
    def get_video(self, request, pk=None):
        try:
            program = InvesterPrograms.objects.get(pk=pk)
            video_path = program.elevator_pitch

            if video_path and os.path.exists(video_path):
                response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'
                return response
            else:
                raise Http404("Video not found")

        except InvesterPrograms.DoesNotExist:
            return Response({'detail': 'Program not found'}, status=404)
        
    #Get Programs Under One Pitch
    
    @action(detail=False, methods=['get'], url_path='pitch_programs')
    def get_pitch_programs(self, request):
        # Retrieve the pitch_id from the query parameters
        pitch_id = request.query_params.get('pitch_id')

        if not pitch_id:
            return Response({'error': 'pitch_id is required.'}, status=400)

        try:
            # Retrieve the pitch instance using the provided pitch_id
            pitch = get_object_or_404(CreatePitch, pk=pitch_id)
            program_id = pitch.program_id
            # Retrieve all programs to which the specific pitch has been applied
            applied_programs = InvesterPrograms.objects.filter(id=program_id)

            # Serialize the applied programs
            serializer = InvesterProgramsSerializer(applied_programs, many=True)
            
            # Return the count and the serialized data
            return Response({
                'count': applied_programs.count(),
                'programs': serializer.data
            }, status=200)
        
        except CreatePitch.DoesNotExist:
            return Response({'detail': 'Pitch not found'}, status=404)