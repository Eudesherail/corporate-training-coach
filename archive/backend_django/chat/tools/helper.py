from agents.models import State, Agent
from users.models import User

def setState(userId, agentName="base", state=0):
    agent = Agent.objects.get(name=agentName)
    created = State.objects.update_or_create(
        user=userId,
        defaults={'current_state': str(state),
        'agent': agent}  
    )
    return created

def getState(userId):
    state = State.objects.get(user=userId)
    return state