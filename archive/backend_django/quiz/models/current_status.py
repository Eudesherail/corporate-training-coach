from django.db import models
from .topic import Topic
from .question import Question

class CurrentStatus(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.question.question}"
