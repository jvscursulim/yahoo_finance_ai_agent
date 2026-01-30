from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from .state import State


llm = ChatOllama(
    model="gemma3:1b"
)


def chat(state: State):

    return {"messages": [llm.invoke(state["messages"])]}

graph = StateGraph(State)
graph.add_node("chat", chat)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

memory = MemorySaver()
agent = graph.compile(checkpointer=memory)
