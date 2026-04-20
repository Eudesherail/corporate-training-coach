from chat.agents.agent import AgentHandler
import chat.tools.tools as tools
import chat.tools.quiz_tools as quizTools
from quiz.models import Topic, CurrentStatus, Question
from chat.prompts.quiz import template, template2
# from utils.service import get_current_status, get_question_by_id, get_topics
# from utils.logger import setup_logger

class AgentClass(AgentHandler):
    
    # Create Quiz Bot
    def __init__(self, state, information="", history="", user=""):
        self.tool_list = [
            quizTools.ExitTool(
                description="Use this if the user wants to exit the quiz",
                userId=user
                ),
            quizTools.GetQuestionTool(userId=user)
        ]
        prompt = ""
        if state == 0:
            prompt = self.template1()
        elif state == 1:
            prompt = self.get_qa(user)
            self.tool_list = [
                quizTools.ExitTool(userId=user),
                quizTools.QuizEvaluationTool(userId=user),
                quizTools.AnotherQuestionTool(userId=user)
            ]
        self.prompt = prompt
        super().__init__(
            prompt=self.prompt,
            model="gpt-4-turbo-preview",
            tool_list=self.tool_list,
            history=history,
            information=information,
            userId=user,
            state=state,
        )

    # Function to execute the Agent
    def execute(self, message):
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            #return f"Es ist leider ein Fehler aufgetreten 😧 Zur Verbesserung des Study Buddys wäre es nett uns dieses Problem zu melden. Fehler: {e}"
            return "Es ist tut mir leid, ich hab dich nicht verstanden! 😧 Könntest du das vielleicht nochmal anders formulieren?"

    def template1(self):
        try:
            topics = Topic.objects.all().values()
            topicsString = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
            prompt = template.replace("{topics}", topicsString)
            return prompt
        except Exception as e:
            print(e)
            return "Error in generating topics list."

    def get_qa(self, user):
        # status = CurrentStatus.objects.get(user=user)
        # qa = Question.objects.get(id=status.question.id)
        # prompt = template2.replace("{query}", qa.question).replace("{answer}", qa.answer)
        # return prompt
        try:
            status = CurrentStatus.objects.get(user=user)
            qa = Question.objects.get(id=status.question.id)
            prompt = template2.replace("{query}", qa.question).replace("{answer}", qa.answer)
            return prompt
        except Exception as e:
            return template2
