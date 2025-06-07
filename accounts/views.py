from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken # Import RefreshToken

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # This calls serializer.create() which returns the user instance

            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                "message": "User registered successfully.",
                "userId": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "tokens": {                         # Add tokens to the response
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print("Registration Errors:", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)