from rest_framework import viewsets
from .models import Topic, Question, CurrentStatus
from .serializers import TopicSerializer, QuestionSerializer, CurrentStatusSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class CurrentStatusViewSet(viewsets.ModelViewSet):
    queryset = CurrentStatus.objects.all()
    serializer_class = CurrentStatusSerializer
