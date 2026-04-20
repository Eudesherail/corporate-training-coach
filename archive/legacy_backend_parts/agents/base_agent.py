from agents.agent import AgentHandler
import tools.tools as tools
import prompts.base as prompts
from utils.logger import setup_logger

class AgentClass(AgentHandler):
    logger = setup_logger(__name__)

    # Create Base Bot
    def __init__(self, state, information = "", history = "", userId = "", token = ""):
        self.tool_list = [
            tools.ask_wiss,
            tools.ask_winfo1,
            tools.DeleteTool(number=userId), 
            tools.SmartGoalTool(userId=userId, token=token),
            tools.QuizTool(userId=userId, token=token),
            tools.youtube,
            tools.ask_features
        ]
        super().__init__(
            prompt = prompts.template,
            model = "gpt-4-1106-preview",
            tool_list = self.tool_list,
            history = history,
            information = information,
            userId = userId,
            token = token,
            state = state,
        ) 
    
    # Function to execute the Agent
    def execute(self, message):
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            logger.error(f"Error during execution: {e}")
            return "Es ist leider ein Fehler aufgetreten 😧 Zur Verbesserung des Study Buddys wäre es nett uns dieses Problem zu melden."

