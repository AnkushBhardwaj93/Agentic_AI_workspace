import os
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

## Define the state of the graph
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain.tools import tool  # Import the tool decorator
from typing import Annotated
from langgraph.graph.message import add_messages
class State(TypedDict):
      messages: Annotated[list[BaseMessage], add_messages]

## model set up
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq
llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
llm

## tool set up

def createTitle(state):
      return{"messages":[llm.invoke(["Create a title for the topic within 10 words"]+state["messages"])]}
      
def createContext(state):
      return{"messages":[llm.invoke(["Create a paragraph  for the topic  within 600 words"]+state["messages"])]}


def create_workflow():
    graph_workflow = StateGraph(State)
    graph_workflow.add_node("title", createTitle)
    graph_workflow.add_node("context", createContext)
    graph_workflow.add_edge(START, "title")
    graph_workflow.add_edge("title", "context")
    graph_workflow.add_edge("context", END)

    agent = graph_workflow.compile()
    return agent

agent = create_workflow()
