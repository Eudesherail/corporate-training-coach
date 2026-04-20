from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Goal

# Get the User model using Django's built-in method
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details. Excludes sensitive information like passwords.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatarName')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only and not returned by the serializer
        }

class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Includes validation for email and username uniqueness.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'avatarName')

    def validate_email(self, value):
        # Ensure the email address is unique
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email address is already in use.")
        return value

    def validate_username(self, value):
        # Ensure the username is unique
        if User.objects.filter(username=value).exists():
            raise ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        # Create a new user instance with the validated data
        return User.objects.create_user(**validated_data)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    class Meta:
        model = User
        fields = ('username', 'avatarName')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair Serializer to include additional user information in the token response.
    """
    def validate(self, attrs):
        # Authenticate the user based on email and password
        user = authenticate(username=attrs.get('email'), password=attrs.get('password'))

        if not user:
            raise AuthenticationFailed('No active account found with the given credentials')

        # Continue with token generation if authentication is successful
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = user.username
        data['userid'] = user.id
        data['avatarName'] = user.avatarName
        data['is_superuser'] = user.is_superuser

        return data

class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for user goals. Links goals with the user who created them.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Goal
        fields = ['id', 'user', 'goal', 'startDate', 'endDate']
        extra_kwargs = {'user': {'read_only': True}}
