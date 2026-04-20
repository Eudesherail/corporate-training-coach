from langchain.tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Type
#from utils.service import set_bot, get_questions_by_topic, set_state, set_current_status, get_current_status, get_topics
from users.models import User, Goal  
from agents.models import State, Agent 
from quiz.models import Topic, CurrentStatus, Question

from chat.tools.helper import setState

class GetQuestionSchema(BaseModel):
    topicId: int = Field(description="number of the topic the user has chosen")        
class GetQuestionTool(BaseTool):
    name: str = "get_question_tool"
    description = """
    Use this if the user has chosen a possible topic from your list. But only if its in your list! 
    Input is the topicId and you will get a question for the user in return. You only need one question for your answer.
    """
    token: str = ""
    userId: int = 0
    args_schema: Type[GetQuestionSchema] = GetQuestionSchema
    def _run(
        self, topicId: int
    ) -> str:
        """Use the tool."""
        topic = Topic.objects.get(id=topicId)
        question = Question.objects.filter(topic=topic).order_by('?').first()
        setState(self.userId, agentName="quiz", state=1)
        user = User.objects.get(id=self.userId)
        CurrentStatus.objects.update_or_create(
            user=user,
            defaults={'topic': topic,
            'question': question}  
        )
        return f"give back this question to the user: {question}"

class QuizEvaluationSchema(BaseModel):
    correct: bool = Field(description="boolean if user has answered correct true/false")
class QuizEvaluationTool(BaseTool):
    name: str = "quiz_evaluation_tool"
    description = "Use this tool if the user has answered the quiz question"
    token: str = ""
    userId: int = 0
    args_schema: Type[QuizEvaluationSchema] = QuizEvaluationSchema
    def _run(
        self, correct: bool
    ) -> str:
        """Use the tool."""
        return f"If the {correct} is false do not show him the correct answer if its true show him.ask the user if he wants to get another question"

class AnotherQuestionTool(BaseTool):
    name: str = "another_question_tool"
    description = """
    Use this if the user has answered the quiz question or wants a new question. 
    No input needed and you will get a question for the user in return. You need only one question
    """
    userId: int = 0
    def _run(
        self, query: str = ""
    ) -> str:
        """Use the tool."""
        user = User.objects.get(id=self.userId)
        state = CurrentStatus.objects.get(user=user)
        topic = Topic.objects.get(name=state.topic)
        qa = Question.objects.filter(topic=state.topic).order_by('?').first()
        question = qa.question
        CurrentStatus.objects.update_or_create(
            user=user,
            defaults={'topic': topic,
            'question': qa}  
        )
        return f"{question}"


# tool to exit the current agent and return to the base agent
class ExitTool(BaseTool):
    name: str = "exit_tool"
    description = "Use this if the user do not want to define a smart goal anymore"
    userId: int = ""
    botId: int = 0
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        agent = Agent.objects.get(name='base')
        created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        return f"Alles klar, dann vielleicht ein anderes mal."


# tool to change the current agent to the goal agent
class QuizTool(BaseTool):
    name: str = "quiz_tool"
    description = "useful for making a quiz. Do not use an input! You will get a list of topics in return."
    userId: int = ""

    def _run(
        self
    ) -> str:
        """Use the tool."""
        topics = Topic.objects.all().values()
        agent = Agent.objects.get(name='quiz')
        state, created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        topicsSting = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
        return f"Zu welchem Thema würdest du denn gerne ein Quizt machen 🎮? /n {topicsSting}"


def getQuestion(userId: int, query: str):
    topic = Topic.objects.get(name=query)
    question = Question.objects.filter(topic=topic).order_by('?').first()
    setState(self.userId, agentName="quiz", state=1)
    user = User.objects.get(id=self.userId)
    CurrentStatus.objects.update_or_create(
        user=user,
        defaults={'topic': topic,
        'question': question}  
    )
    return question

def findTopicByName(topics, name):
    for topic in topics:
        if topic['name'] == name:
            return topic
    return None