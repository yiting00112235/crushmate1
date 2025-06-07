from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # Add JSONField for interests
    interests = models.JSONField(default=list, blank=True, null=True) # Stores a list of strings

    def __str__(self):
        return f"Profile of {self.user.username}"

class ProfilePhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='profile_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False) # True if this is the main profile picture

    def __str__(self):
        return f"{self.user.username} - {self.image.name}"