from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import Profile, ProfilePhoto
from .serializers import ProfileSerializer, ProfileUpdateSerializer, ProfilePhotoSerializer
from django.shortcuts import get_object_or_404

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update the authenticated user's profile.
    GET: Returns the user's profile (user details, bio, interests, photos).
    PUT/PATCH: Updates the user's bio and/or interests.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Profile is created via UserRegistrationSerializer or a signal
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer # Use this for updating bio/interests
        return ProfileSerializer # Use this for GET

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileSerializer(instance) # Always use ProfileSerializer for GET
        return Response(serializer.data)

class ProfilePhotoUploadAPIView(generics.CreateAPIView):
    """
    API endpoint to upload a new profile photo for the authenticated user.
    """
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # For file uploads

    def perform_create(self, serializer):
        user = self.request.user
        # Limit number of photos
        if ProfilePhoto.objects.filter(user=user).count() >= 9:
            # Using DRF's validation error is better for APIs
            raise serializers.ValidationError({"detail": "Maximum of 9 photos allowed."}, code=status.HTTP_400_BAD_REQUEST)
        
        # If this is the first photo, make it the main one
        is_first_photo = not ProfilePhoto.objects.filter(user=user).exists()
        serializer.save(user=user, is_main=is_first_photo if is_first_photo else serializer.validated_data.get('is_main', False))


class ProfilePhotoDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    API endpoint to retrieve or delete a specific profile photo.
    """
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'photo_id' # Matches the URL pattern

    def get_queryset(self):
        # Ensure users can only access/delete their own photos
        return ProfilePhoto.objects.filter(user=self.request.user)

    # Add method to set a photo as main
    def patch(self, request, *args, **kwargs): # Or PUT if you prefer
        photo = self.get_object()
        ProfilePhoto.objects.filter(user=request.user, is_main=True).update(is_main=False)
        photo.is_main = True
        photo.save()
        serializer = self.get_serializer(photo)
        return Response(serializer.data)