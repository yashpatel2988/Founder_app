from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FounderProfile
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .utils import extract_user_id  # Import the utility function for user ID extraction

class UserProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        List all active user profiles.
        
        Args:
            request (Request): The HTTP request object.
        
        Returns:
            Response: A response containing serialized user profile data.
        """
        queryset = FounderProfile.objects.filter(is_active=True)  # Filter active profiles
        serializer = UserProfileSerializer(queryset, many=True)  # Serialize the queryset
        return Response(serializer.data)  # Return serialized data

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific user profile by ID.
        
        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the user profile to retrieve.
        
        Returns:
            Response: A response containing the serialized user profile data.
        """
        user_profile = get_object_or_404(FounderProfile, pk=pk, is_active=True)  # Get user profile or 404
        serializer = UserProfileSerializer(user_profile)  # Serialize the user profile
        return Response(serializer.data)  # Return serialized data

    def update_profile(self, request):
        """
        Update a user profile based on the provided user ID.
        
        Args:
            request (Request): The HTTP request object containing user ID and update data.
        
        Returns:
            Response: A response with the updated profile data or errors.
        """
        user_id = extract_user_id(request.query_params.get('user_id'))  # Extract user ID
        if user_id is None:
            return Response({"error": "user_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)  # Handle invalid user ID
        
        user_profile = get_object_or_404(FounderProfile, pk=user_id, is_active=True)  # Get user profile or 404
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)  # Serialize with update data
        if serializer.is_valid():
            serializer.save()  # Save the updated profile
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

    def soft_delete(self, request):
        """
        Soft delete a user profile by marking it as inactive.
        
        Args:
            request (Request): The HTTP request object containing user ID.
        
        Returns:
            Response: A response confirming that the user account has been marked as deleted.
        """
        user_id = extract_user_id(request.query_params.get('user_id'))  # Extract user ID
        if user_id is None:
            return Response({"error": "user_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)  # Handle invalid user ID
        
        user_profile = get_object_or_404(FounderProfile, pk=user_id, is_active=True)  # Get user profile or 404
        user_profile.is_active = False  # Mark user profile as inactive
        user_profile.save()  # Save changes
        return Response({"message": "User account marked as deleted"}, status=status.HTTP_200_OK)  # Confirm deletion

class UserDetailView(APIView):
    def get(self, request):
        """
        Retrieve details of a specific user profile based on the user ID.
        
        Args:
            request (Request): The HTTP request object containing user ID.
        
        Returns:
            Response: A response containing the serialized user profile data.
        """
        user_id = extract_user_id(request.query_params.get('user_id'))  # Extract user ID
        if user_id is None:
            return Response({"error": "user_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)  # Handle invalid user ID
        
        user_profile = get_object_or_404(FounderProfile, id=user_id, is_active=True)  # Get user profile or 404
        serializer = UserProfileSerializer(user_profile)  # Serialize the user profile
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data

class UserRegistrationView(APIView):
    
    def post(self, request):
        """
        Register a new user or return existing user details if already registered.
        
        Args:
            request (Request): The HTTP request object containing user registration data.
        
        Returns:
            Response: A response with the user ID and a success message, or errors.
        """
        data = JSONParser().parse(request)  # Parse the incoming data
        login_id = data.get('login_id')  # Extract login ID
        
        if not login_id:
            return Response({"error": "login_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)  # Handle missing login ID
        
        user_profile = FounderProfile.objects.filter(login_id=login_id).first()  # Check if user already exists
        if user_profile:
            return Response({"user_id": user_profile.id, "message": "User already registered"}, status=status.HTTP_200_OK)  # Return existing user ID
        else:
            serializer = UserProfileSerializer(data=data)  # Serialize new user data
            if serializer.is_valid():
                user_profile = serializer.save()  # Save new user profile
                return Response({"user_id": user_profile.id, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)  # Return new user ID
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid
