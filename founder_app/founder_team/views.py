from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from .models import FounderTeamsProfile
from .serializers import TeamInviteSerializer

class TeamInviteView(APIView):
    def post(self, request):
        serializer = TeamInviteSerializer(data=request.data)
        if serializer.is_valid():
            daftar_id = serializer.validated_data['daftar'].id
            token = get_random_string(length=32)
            serializer.save(invitation_token=token)
            invite_url = request.build_absolute_uri(reverse('accept-invite', args=[token]))
            return Response({
                'invite': serializer.data,
                'invite_url': invite_url
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptInviteView(APIView):
    def get(self, request, token):
        try:
            invite = FounderTeamsProfile.objects.get(invitation_token=token, is_active=False)
            invite.is_active = True
            invite.save()
            return Response({"message": "You have successfully joined the team."}, status=status.HTTP_200_OK)
        except FounderTeamsProfile.DoesNotExist:
            return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
