import importlib
import os
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from users.models import Goal
from agents.models import State
from langchain.memory import PostgresChatMessageHistory

# Load the environment variables from the .env file
env_path="../.env"
load_dotenv(env_path)

# Database connection string for PostgresChatMessageHistory
DB_CONNECTION_STRING = os.getenv('DATABASE_URL')

class AgentFactory:
    @staticmethod
    def create_agent(user):
        """Creates an agent for the given user object.

        This method retrieves the user's goal and state, loads their chat history,
        and dynamically imports and creates an agent instance based on the user's current state.

        Args:
            user: The user object for whom to create the agent.

        Returns:
            An instance of the agent class if successful, None otherwise.

        Raises:
            ValueError: If the goal, agent, or state does not exist.
        """
        try:
            # Retrieve the user's goal and state from the database
            user_goal = Goal.objects.get(user=user)
            user_state = State.objects.get(user=user)

            # Assemble user information into a string format
            information = f"Username: {user.username},\nUser Goal: {str(user_goal)}"
    
            # Load the user's chat message history
            message_history = PostgresChatMessageHistory(
                connection_string=DB_CONNECTION_STRING, session_id=str(user.id)
            )

            # Dynamically import the agent module and class based on the agent's name
            agent_module_name = f"chat.agents.{user_state.agent}_agent"
            agent_module = importlib.import_module(agent_module_name)
            agent_class = getattr(agent_module, "AgentClass")

            # Instantiate and return the agent
            return agent_class(user_state.current_state, information, message_history, user.id)

        except ObjectDoesNotExist as e:
            raise ValueError(f"Required object not found: {e}")
        except ImportError as e:
            raise ValueError(f"Failed to import agent module: {e}")
        except AttributeError as e:
            raise ValueError(f"AgentClass not found: {e}")
        except Exception as e:
            raise ValueError("An unexpected error occurred during agent creation.")
