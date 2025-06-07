# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from profilepage.models import Profile
from rest_framework.validators import UniqueValidator # <--- ADD THIS LINE

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'username': {
                'validators': [
                    UniqueValidator( # Now UniqueValidator should be recognized
                        queryset=User.objects.all(),
                        lookup='iexact',
                        message="A user with that username already exists."
                    )
                ]
            },
            'email': {
                'validators': [
                    UniqueValidator( # And here as well
                        queryset=User.objects.all(),
                        lookup='iexact',
                        message="A user with that email already exists."
                    )
                ]
            }
        }

    def validate_username(self, value):
        if any(c.isupper() for c in value):
            raise serializers.ValidationError("Username cannot contain uppercase letters.")
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        profile, created = Profile.objects.get_or_create(user=user)
        return user