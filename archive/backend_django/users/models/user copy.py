from django.db import models
from .goal import Goal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Goal.objects.create(user=user, goal=None, startDate=None, endDate=None)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            password=password,
            username=username
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    avatarName = models.CharField(max_length=255, blank=True, default='Mensch-1')
#    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='users')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Fügen Sie related_name Argumente hinzu
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='Benutzergruppen',
        blank=True,
        help_text='Die Gruppen, zu denen dieser Benutzer gehört.',
        related_name="custom_user_set",  # Ändern Sie 'user_set' zu 'custom_user_set'
        related_query_name="custom_user",  # Optional: Ändern Sie 'user' zu 'custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='Benutzerberechtigungen',
        blank=True,
        help_text='Spezifische Berechtigungen für diesen Benutzer.',
        related_name="custom_user_set",  # Ändern Sie 'user_set' zu 'custom_user_set'
        related_query_name="custom_user",  # Optional: Ändern Sie 'user' zu 'custom_user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
