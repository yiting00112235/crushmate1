# django_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from navigation import views as nav_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/accounts/', include('accounts.urls')), # Your registration API
    # Allauth URLs for web-based authentication (login, signup HTML pages, etc.)
    path('accounts/', include('allauth.urls')), 
    path('api/v1/profilepage/', include('profilepage.api_urls')),
    # Your new API URLs for the accounts app (for mobile app, etc.)
    # This will make your registration API available at /api/v1/accounts/register/
    path('api/v1/accounts/', include('accounts.urls', namespace='accounts_api')), # <-- ADD THIS LINE

    # Original page navigation links
    path('', include('navigation.urls')),
    path('home/', nav_views.home, name='home'),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
    #settings
    path('settings/bio/', include('bio.urls')),
    path('settings/course/', include('course.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)