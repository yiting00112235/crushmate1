# profilepage/api_urls.py
from django.urls import path
from .api_views import (
    UserProfileAPIView, 
    ProfilePhotoUploadAPIView,
    ProfilePhotoDetailAPIView
)

app_name = 'profilepage_api'

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('photos/upload/', ProfilePhotoUploadAPIView.as_view(), name='profilephoto-upload'),
    path('photos/<int:photo_id>/', ProfilePhotoDetailAPIView.as_view(), name='profilephoto-detail'),
    # The PATCH to set main photo will use the 'profilephoto-detail' URL
]