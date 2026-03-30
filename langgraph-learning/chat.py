from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.language_models.fake import FakeListLLM


llm = FakeListLLM(responses=[
    "Hello! I am fake LLM 🤖",
    "Second response"
])


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state["messages"])   # ✅ FIXED
    return {"messages": [response]}            # ✅ USE LLM RESPONSE


def sampleNode(state: State):
    return {"messages": ["hi this is a message from sample node"]}


# Build graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

graph = graph_builder.compile()


# Invoke graph
initial_state = {
    "messages": ["hi this is invoke state schema passing to start graph"]
}

updated_state = graph.invoke(initial_state)

print("updated state:", updated_state)