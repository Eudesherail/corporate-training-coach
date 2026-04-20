from django.db import models
from users.models import User
from agents.models import Agent

class State(models.Model):
    current_state = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='states')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return str(self.current_state)