from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignUpView, SignInView, UserDetailView, UpdateUserProfileView, GoalViewSet, DeleteUserMessages, InviteSSOAuth

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')

# Define the URL patterns for the API
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),  # Route for user signup
    path('signin/', SignInView.as_view(), name='signin'),  # Route for user signin
    path('user/', UserDetailView.as_view(), name='userDetails'),  # Route to retrieve user details
    path('profile/', UpdateUserProfileView.as_view(), name='userUpdate'),  # Route to update user profile
    path('delete_messages/', DeleteUserMessages.as_view(), name='delete-messages'),  # Route to delete user messages
    path('inviteee', InviteSSOAuth.as_view(), name='invite-auth'),  # Route to authenticate user with invite
    path('', include(router.urls)),  # Include the URLs from the GoalViewSet
]
