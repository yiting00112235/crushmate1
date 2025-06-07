# profilepage/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ProfilePhoto

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for User model details (read-only for profile display).
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        read_only_fields = fields # Make all these fields read-only via this serializer


class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = ['id', 'image', 'is_main', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at'] # image and is_main can be set/modified

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model, including nested User details and photos.
    """
    user = UserDetailsSerializer(read_only=True) # Read-only nested user details
    photos = ProfilePhotoSerializer(many=True, read_only=True, source='user.photos') # Read-only list of photos
    
    # For updating, we'll only allow bio and interests
    bio = serializers.CharField(required=False, allow_blank=True, style={'base_template': 'textarea.html'})
    interests = serializers.ListField(
       child=serializers.CharField(max_length=100), 
       required=False, 
       allow_empty=True
    )

    class Meta:
        model = Profile
        # Fields to be returned when GETTING profile
        fields = ['user', 'bio', 'interests', 'photos'] 
        # Fields that can be UPDATED (Note: 'user' and 'photos' are handled separately or read-only here)
        # When updating, we'll create a separate serializer or handle fields in the view.

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for updating Profile (bio and interests).
    """
    bio = serializers.CharField(required=False, allow_blank=True, style={'base_template': 'textarea.html'})
    interests = serializers.ListField(
       child=serializers.CharField(max_length=100, allow_blank=True), # allow blank strings in list
       required=False, 
       allow_empty=True
    )

    class Meta:
        model = Profile
        fields = ['bio', 'interests']