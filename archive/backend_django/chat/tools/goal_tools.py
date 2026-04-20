from langchain.tools import tool, BaseTool
from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field

from users.models import Goal
from agents.models import State, Agent


class ExtractGoalSchema(BaseModel):
    """Schema for the tool's arguments."""

    goal: str = Field(
        description="The smart goal to be extracted from the conversation"
    )
    date: str = Field(
        description="The extracted end date for the goal in the format yyyy-mm-dd"
    )


class ExtractGoal(BaseTool):
    """A tool for extracting and storing a smart goal from a conversation."""

    name: str = "extract_goal_tool"
    description: str = "Use this if the user has defined a smart goal."
    userId: int = ""  # UserId for the current user
    dateToday: datetime = datetime.now().date()  # Current date
    args_schema: Type[ExtractGoalSchema] = ExtractGoalSchema  # Schema for the tool's arguments

    def _run(
        self, goal: str, date: str
    ) -> str:
        """Executes the tool's logic."""
        # Get the base agent
        agent = Agent.objects.get(name="base")

        # Update or create the user's state
        state, created = State.objects.update_or_create(
            user=self.userId,
            defaults={
                "current_state": 0,  # Set the user's current state to 0
                "agent": agent,  # Set the user's agent to the base agent
            },
        )

        # Update or create the goal for the user
        created = Goal.objects.update_or_create(
            user=self.userId,
            defaults={
                "goal": goal,
                "startDate": self.dateToday,  # Set the start date to today's date
                "endDate": date,  # Set the end date to the specified date
            },
        )

        # Return the success message
        return f"Super! Ich habe dein Ziel {goal} gespeichert."

# tool to exit the current agent and return to the base agent
class ExitTool(BaseTool):
    name: str = "exit_tool"
    description = "Use this if the user do not want to define a smart goal anymore. No input needed and you just answer with a message like u get from the tool."
    userId: int = ""
    botId: int = 0
    def _run(
        self, query: str = "exit"
    ) -> str:
        """Use the tool."""
        agent = Agent.objects.get(name='base')
        created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        return f"Alles klar, dann vielleicht ein anderes mal."