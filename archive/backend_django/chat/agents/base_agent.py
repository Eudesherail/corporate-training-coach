from chat.agents.agent import AgentHandler
from quiz.models import Topic
import chat.tools.tools as tools
import chat.tools.quiz_tools as quizTools
import chat.prompts.base as prompts

class AgentClass(AgentHandler):

    # Create Base Bot
    def __init__(self, state, information = "", history = "", userId = ""):
        self.tool_list = [
            tools.ask_wiss,
            tools.ask_winfo1,
            tools.SmartGoalTool(userId=userId),
            quizTools.GetQuestionTool(userId=userId),
            tools.youtube,
            tools.ask_features
        ]
        self.template = prompts.template
        prompt = self.createPrompt()
        super().__init__(
            prompt = prompt,
            model = "gpt-4-turbo-preview",
            tool_list = self.tool_list,
            history = history,
            information = information,
            userId = userId,
            state = state,
        ) 
    
    # Function to execute the Agent
    def execute(self, message):      
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            #return f"Es ist leider ein Fehler aufgetreten 😧 Zur Verbesserung des Study Buddys wäre es nett uns dieses Problem zu melden. Fehler: {e}"
            return "Es ist tut mir leid, ich hab dich nicht verstanden! 😧 Könntest du das vielleicht nochmal anders formulieren?"
    def createPrompt(self):
        try:
            topics = Topic.objects.all().values()
            topicsString = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
            prompt = self.template.replace("{topics}", topicsString)
            return prompt
        except Exception as e:
            print(e)
            return f"Error in generating topics list: {e}"