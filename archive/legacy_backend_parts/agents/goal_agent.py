from prompts.goal import template4
from agents.agent import AgentHandler
import tools.tools as tools
from datetime import datetime
from utils.logger import setup_logger

class AgentClass(AgentHandler):
    logger = setup_logger(__name__)

    def __init__(self, state: int, information="", history="", userId="", token=""):
        tool_list = [
            tools.ExtractGoal(userId=userId, token=token),
            tools.ExitTool(userId=userId, token=token),
        ]
        current_date = datetime.now().date()
        prompt = template4.replace("{date}", str(current_date))
        super().__init__(
            prompt=prompt,
            model="gpt-3.5-turbo",
            tool_list=tool_list,
            history=history,
            information=information,
            userId=userId,
            token=token,
            state=state,
        )

    def execute(self, message):
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            self.logger.error(f"Error during execution: {e}")
            return "Ein Fehler ist aufgetreten. Bitte melden Sie dieses Problem zur Verbesserung des Dienstes."


