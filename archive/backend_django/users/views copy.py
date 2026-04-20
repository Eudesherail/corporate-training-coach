from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from .models import User, Goal
from agents.models import Agent, State
from .serializers import UserSerializer, UserSignUpSerializer, UserProfileUpdateSerializer, MyTokenObtainPairSerializer, GoalSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Retrieve or create the base Agent
            base_agent, created = Agent.objects.get_or_create(
                name = 'base',
                defaults={
                    'description': 'Die erste Station des Studdy Budys', # If the agent needs to be created
                }  
            )

            # Create the default State for the new user
            State.objects.create(user=user, current_state=0, agent=base_agent)

            # Generate token for the new user
            token_serializer = MyTokenObtainPairSerializer.get_token(user)
            return Response({
                'token': str(token_serializer.access_token),
                'refresh': str(token_serializer),
                'userId': user.id,
                'username': user.username,
                'avatarName': user.avatarName
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Check for specific errors and return a simplified message
            if 'email' in e.detail and 'unique' in str(e.detail['email']):
                return Response({'message': 'Die E-Mail Adresse ist bereits vergeben.'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in e.detail and 'unique' in str(e.detail['username']):
                return Response({'message': 'Der Nutzername ist bereits vergeben.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Ein Fehler ist aufgetreten.'}, status=status.HTTP_400_BAD_REQUEST)

class SignInView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        print(request)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Überprüfen, ob der Benutzer authentifiziert ist
        if isinstance(self.request.user, AnonymousUser):
            # Ggf. leeren QuerySet zurückgeben, wenn der Benutzer nicht authentifiziert ist
            return Goal.objects.none()
        else:
            # Benutzer ist authentifiziert, fahren Sie mit dem normalen Verhalten fort
            return Goal.objects.filter(user=self.request.user)