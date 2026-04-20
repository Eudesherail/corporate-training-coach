from langchain.agents import AgentExecutor
#from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.format_scratchpad import format_to_openai_function_messages

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
#from langchain.chat_models import ChatOpenAI
#from langchain_community.adapters.openai import Chat
from langchain_openai import ChatOpenAI

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools.render import format_tool_to_openai_function

import os
from dotenv import load_dotenv
import importlib

#import tools.tools as tools

def load_environment_variables(env_path="../.env"):
    load_dotenv(env_path)
    openai_key = os.getenv('OPENAI_KEY')
    if not openai_key:
        raise EnvironmentError("OPENAI_KEY not found in environment variables")
    return openai_key

class AgentHandler:
    def __init__(self, prompt, model, tool_list, history, information, userId, state):
        try:
            # Load openai key
            self.openai_key = load_environment_variables()
        except EnvironmentError:
            raise ValueError("OPENAI_KEY not found in environment variables")
        try:
            # Create a list of functions fot the bot
            self.tool_list = tool_list
            self.functions = [convert_to_openai_function(f) for f in self.tool_list] #convert the langchain to openai functions

            # Create llm and insert functions
            self.llm = ChatOpenAI(
                openai_api_key=self.openai_key,
                temperature=0.5,
                model_name=model
            ).bind(functions=self.functions)

            self.information = information
            self.userId = userId

            # Create memory
            self.memory = ConversationBufferMemory(
                chat_memory=history, 
                return_messages=True,
                memory_key="chat_history")

            # Create Prompt          
            #prompt = importlib.import_module("prompts." + prompt_name) # Importiert den Prompt dynamisch basierend auf dem übergebenen Namen
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", prompt),
                #MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                
            ])
   
            partial_variables = {
                "tools": self._convert_tools(self.tool_list),
                "tool_names": ", ".join(tool.name for tool in self.tool_list),
                "user_information": self.information,
            }

            # Create the AgentChain
            self.chain = RunnablePassthrough.assign(
                agent_scratchpad = lambda x: format_to_openai_function_messages(x["intermediate_steps"])
            ) | self.prompt.partial(**partial_variables) | self.llm | OpenAIFunctionsAgentOutputParser()
            

            self.state = state

            # Create Executor for the Agent
            self.agent = AgentExecutor(agent=self.chain, tools=self.tool_list, verbose=True, memory=self.memory, max_iterations=3,)

        except Exception as e:

            raise ValueError("An unexpected error occurred during agent initializing.") 

    # Function to make a list of the tool names
    @staticmethod
    def _convert_tools(tools):
        return "\n".join(f"{tool.name}: {tool.description}" for tool in tools)
    @staticmethod
    def _convert_intermediate_steps(intermediate_steps):
        log = ""
        for action, observation in intermediate_steps:
            log += (
                f"<tool>{action.tool}</tool><tool_input>{action.tool_input}"
                f"</tool_input><observation>{observation}</observation>"
            )
        return log