import importlib
from langchain.memory import PostgresChatMessageHistory
from utils.service import get_goal, get_token, DB, set_bot, get_bot, get_state, set_goal, delete_session
from utils.models import MessageData, DeleteData
from utils.helper import userInformation
from utils.logger import setup_logger

class AgentFactory:
    logger = setup_logger(__name__)
    @staticmethod
    def create_agent(userName, userId, token):
        try:
            # Fetch the goal from the backend
            userGoalData = get_goal(token, userId)
            userGoal = userGoalData["goal"] if userGoalData != "none" else "none"

            # Create the user informations sting for the prompt
            information = userInformation(userName, userGoal)

            # Fetch the user agent from the backend
            userAgent = get_bot(token, userId)
            userAgentName = userAgent['name']

            # Fetch the state from the backend
            userState = get_state(token, userId, userAgent["botId"])
            userState = userState if userState is not None else 0

            # Load user history
            message_history = PostgresChatMessageHistory(
                connection_string=DB, session_id=userId
            )

            # Import the agent module based on the name
            agent_module = importlib.import_module(f"agents.{userAgentName}_agent")

            # Create an instance of the agent class
            agent_class = getattr(agent_module, "AgentClass")
            return agent_class(int(userState), information, message_history, userId, token)

        except ImportError as e:
            logger.error(f"ImportError occurred: {e}")
            raise ValueError(f"Agent class '{userAgentName}' not found or faulty.")
        except AttributeError as e:
            logger.error(f"AttributeError occurred: {e}")
            raise ValueError(f"Agent class '{userAgentName}' not found or faulty.")
        except Exception as e:
            logger.error(f"Unexpected error occurred during agent creation: {e}")
            raise ValueError("An unexpected error occurred during agent creation.")
