from django.urls import path
from .views import UserRegistrationAPIView

app_name = 'accounts' # Namespace for these API urls

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register-api'),
    # path('login/', YourLoginApiView.as_view(), name='user-login-api'), # Example for later
]