from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Goal


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatarName')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'avatarName')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Diese E-Mail-Adresse wird bereits verwendet.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Dieser Benutzername wird bereits verwendet.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatarName')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Benutzername und Passwort aus den Anmelde-Attributen holen
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        # Benutzer mit Django's authenticate-Methode überprüfen
        user = authenticate(username=email, password=password)

        # Benutzerdefinierte Fehlermeldungen
        def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise ValidationError("This email address is already in use.")
            return value

        def validate_username(self, value):
            if User.objects.filter(username=value).exists():
                raise ValidationError("This username is already taken.")
            return value

        # Weiter mit der normalen Token-Generierung, wenn alles in Ordnung ist
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['userid'] = self.user.id

        return data

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'goal', 'startDate', 'endDate']
