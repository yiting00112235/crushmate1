from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", include('chat.urls'), name="chat"),
    path("settings/", include('settingsapp.urls'), name="settings"),
    path("profilepage/", include('profilepage.urls'), name="profilepage"),
    path("match/", include('match.urls', namespace='match')),
]
