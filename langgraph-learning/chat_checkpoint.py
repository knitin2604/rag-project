from typing_extensions import TypedDict
from typing import Annotated
import atexit

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver

from langchain_core.language_models.fake import FakeListLLM


# Fake LLM (for testing)
llm = FakeListLLM(responses=[
    "Hello! I am fake LLM 🤖",
    "Second response"
])


# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Chatbot node
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# Build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# Compile graph with MongoDB checkpointer
def compile_graph_with_checkpointer():
    DB_URI = "mongodb://admin:admin@localhost:27017/lg?authSource=admin"

    # Create context manager
    saver_cm = MongoDBSaver.from_conn_string(DB_URI)

    # Enter manually (IMPORTANT)
    checkpointer = saver_cm.__enter__()

    # Ensure clean shutdown
    atexit.register(lambda: saver_cm.__exit__(None, None, None))

    graph = graph_builder.compile(checkpointer=checkpointer)

    return graph


# Create graph
graph_with_checkpointer = compile_graph_with_checkpointer()


# Config (thread-based memory)
config = {
    "configurable": {
        "thread_id": "nitin"
    }
}


# Invoke graph
updated_state = graph_with_checkpointer.invoke(
    {"messages": ["hey my name is nitin yadav"]},
    config,
)

print("updated state:", updated_state)