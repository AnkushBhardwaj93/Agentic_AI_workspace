import os
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

#`# Load environment variables from .env file
# This is only needed if you are using a .env file to store your API keys`
load_dotenv()

#os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")

# Initialize the Groq model
# This is only needed if you are using the Groq model
#llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
#llm

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")
llm


## Define the state of the graph
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain.tools import tool  # Import the tool decorator
from typing import Annotated
from langgraph.graph.message import add_messages 

class State(TypedDict):
      messages: Annotated[list[BaseMessage], add_messages]


## make a tool calling agent
def make_alnerate_graph():
    """Make a tool calling agent """
    @tool
    def add(a: int, b: int) -> int:
        """
        Adds two integers and returns the result.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The sum of a and b.
        """
        return a + b

    ## tools
    tool_node = ToolNode([add])
    model_with_tools = llm.bind_tools([add]) 

    ## call the model with tools
    def call_model(state):
        return {"messages": [model_with_tools.invoke(state["messages"])]}
    
    def should_continue(state: State):
        """
        Determines the next step in the state graph based on the last message.

        Args:
            state (State): The current state of the graph, which includes a list of messages.

        Returns:
            str: Returns "tools" if the last message indicates a tool call; otherwise, returns END.
        """
        # Check if the last message in the state's messages list is a tool call
        if state["messages"][-1].tool_call:
            # If it is a tool call, return "tools" to indicate the next step involves tools
            return "tools"
        else:
            # Otherwise, return END to indicate the end of the graph
            return END

    graph_workflow = StateGraph(State)
    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_edge("agent", "tools")
    graph_workflow.add_conditional_edges("agent", should_continue)

    agent = graph_workflow.compile()
    return agent

agent = make_alnerate_graph()
