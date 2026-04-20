from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, QuestionViewSet, CurrentStatusViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'current-status', CurrentStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
