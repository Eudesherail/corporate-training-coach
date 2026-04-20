from django.db import models
from .topic import Topic

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    chapter = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
