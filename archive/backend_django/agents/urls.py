from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, StateViewSet

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'states', StateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]