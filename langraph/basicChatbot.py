from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

llm =ChatGroq(model="gpt-4", temperature=0.0, max_tokens=1000, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)

class State(TypedDict):
      message: Annotated[list, add_messages]

def chatbot(state: State):
      return{"messages":[llm.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

from IPython.display import Image, display
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass