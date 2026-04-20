from rest_framework import status, generics, viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from django.db import connection
from .models import User, Goal
from agents.models import Agent, State
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    UserProfileUpdateSerializer,
    MyTokenObtainPairSerializer,
    GoalSerializer,
)
import logging
import requests
import jwt

# Erstellen Sie ein Logger-Objekt
logger = logging.getLogger(__name__)

class SignUpView(generics.CreateAPIView):
    """
    A view for user registration. Handles user creation and initial setup for new users.
    """
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Retrieve or create the base agent, providing a default if it doesn't exist.
            base_agent = Agent.objects.get(name='base')
            
            # Create the default state for the new user.
            State.objects.create(user=user, current_state=0, agent=base_agent)

            # Generate token for the new user.
            token_serializer = MyTokenObtainPairSerializer.get_token(user)
            return Response({
                'token': str(token_serializer.access_token),
                'refresh': str(token_serializer),
                'userId': user.id,
                'username': user.username,
                'avatarName': user.avatarName,
                'is_superuser': user.is_superuser
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Simplify error messages for common validation errors.
            if 'email' in e.detail and 'unique' in str(e.detail['email']):
                return Response({'message': 'Die E-Mail Adresse ist bereits vergeben.'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in e.detail and 'unique' in str(e.detail['username']):
                return Response({'message': 'Der Benutzername ist bereits vergeben.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'An error occurred.'}, status=status.HTTP_400_BAD_REQUEST)

class SignInView(TokenObtainPairView):
    """
    A view for user sign in. Utilizes JSON Web Tokens (JWT) for authentication.
    """
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            # Customize the response for authentication failures
            return Response({'message': 'Benutzername oder Passwort falsch!'}, status=status.HTTP_400_BAD_REQUEST)

        # If authentication is successful, proceed with the normal token generation process
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    """
    A view for fetching the details of the current user. Requires authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current user instance.
        return self.request.user

class UpdateUserProfileView(generics.UpdateAPIView):
    """
    A view for updating user profile information. Supports partial updates.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # Ensure partial update
        return self.update(request, *args, **kwargs)
    
    def get_object(self):
        # Return the current user instance for profile updates.
        return self.request.user

class GoalViewSet(viewsets.ModelViewSet):
    """
    A viewset for creating, retrieving, updating, and deleting user goals. Requires authentication.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return goals for the current user, ensuring only authenticated users can view their goals.
        """
        if isinstance(self.request.user, AnonymousUser):
            return Goal.objects.none()  # Return an empty queryset for unauthenticated users
        return Goal.objects.filter(user=self.request.user)  # Filter goals by the current user

    def perform_create(self, serializer):
        """
        Associate the new goal with the current user.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new goal or update the existing one for the user.
        """
        # Check if the user already has a goal
        goal, created = Goal.objects.get_or_create(user=request.user)
        
        # Initialize the serializer instance with the existing goal and the request data
        serializer = self.get_serializer(goal, data=request.data, partial=not created)
        serializer.is_valid(raise_exception=True)
        
        # Save the serializer which will either update the existing goal or create a new one
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Determine the appropriate status code (201 for created, 200 for updated)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        return Response(serializer.data, status=status_code, headers=headers)


class DeleteUserMessages(APIView):
    # Apply JWT Authentication
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_id = str(request.user.id)  # Get user ID from JWT token

        try:
            # Execute raw SQL to delete user messages
            with connection.cursor() as cursor:
                query = "DELETE FROM message_store WHERE session_id = %s"
                cursor.execute(query, [user_id])

            # Return a success response
            return Response({"status": "success", "message": "Messages deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            # Return an error response if something goes wrong
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InviteSSOAuth(APIView):
    def post(self, request, *args, **kwargs):
        logger.debug(request)
        invite_code = request.data.get('inviteCode')
        logger.debug(f"Received inviteCode: {invite_code}")

        if not invite_code:
            return Response({'error': 'Invite code is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = self.get_invite_access_token(invite_code)
            decoded_token = self.decode_invite_token(access_token)
            user = self.authenticate_or_create_user(decoded_token)
            token = MyTokenObtainPairSerializer.get_token(user)

            return Response({
                'token': str(token.access_token),
                'refresh': str(token),
                'userId': user.id,
                'username': user.username,
                'is_superuser': user.is_superuser,
                'avatarName': user.avatarName
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_invite_access_token(self, code):
        url = "https://auth.invite-toolcheck.de/oauth2/token"
        data = {
            "client_id": "a72e8cd0-99a0-4934-881c-cc34137c805e",
            "client_secret": "T86O8GV7DoSa0zUmyQu0",
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://stubu.oks.de/auth-callback"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()['id_token']
        else:
            # Erweitertes Logging für Fehlerfälle
            logger.error(f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}")
            raise Exception(f"Failed to obtain access token. Status code: {response.status_code}")

    def decode_invite_token(self, access_token):
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            return decoded
        except jwt.PyJWTError as e:
            raise Exception("Failed to decode JWT token") from e

    def authenticate_or_create_user(self, decoded_token):
        email = decoded_token.get("email")
        given_name = decoded_token.get("given_name")
        family_name = decoded_token.get("family_name")
        username = f"{given_name} {family_name}"

        if not User.objects.filter(email=email).exists():
            logger.error("niemand da")
            user = User.objects.create(email=email, username=username)
            # Retrieve or create the base agent, providing a default if it doesn't exist.
            base_agent = Agent.objects.get(name='base')
                
            # Create the default state for the new user.
            State.objects.create(user=user, current_state=0, agent=base_agent)
            Goal.objects.create(user=user)
            return user
        else:
            return User.objects.get(email=email)

    def generate_jwt_for_user(self, user):
        # Implement based on your JWT setup
        pass
