from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    messages: Annotated[list, add_messages]


# -------------------------
# Nodes
# -------------------------

def router(state: State):
    """Decides where to go next based on user input"""
    last_message = state["messages"][-1].lower()

    if "weather" in last_message:
        return {"route": "weather_node"}
    elif "joke" in last_message:
        return {"route": "joke_node"}
    else:
        return {"route": "default_node"}


def weather_node(state: State):
    return {"messages": ["🌦️ Weather is sunny 25°C"]}


def joke_node(state: State):
    return {"messages": ["😂 Why did the dev quit? Because of too many bugs!"]}


def default_node(state: State):
    return {"messages": ["🤖 I can help with weather or jokes!"]}


# -------------------------
# Graph Builder
# -------------------------

graph_builder = StateGraph(State)

graph_builder.add_node("router", router)
graph_builder.add_node("weather_node", weather_node)
graph_builder.add_node("joke_node", joke_node)
graph_builder.add_node("default_node", default_node)

# Start → Router
graph_builder.add_edge(START, "router")


# -------------------------
# Conditional Routing
# -------------------------

def route_decision(state: State):
    """Reads route from router output"""
    return state["route"]


graph_builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "weather_node": "weather_node",
        "joke_node": "joke_node",
        "default_node": "default_node",
    },
)

# End all paths
graph_builder.add_edge("weather_node", END)
graph_builder.add_edge("joke_node", END)
graph_builder.add_edge("default_node", END)


graph = graph_builder.compile()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    inputs = [
        "tell me weather",
        "tell me a joke",
        "hello",
    ]

    for user_input in inputs:
        print("\n--- Input:", user_input)

        result = graph.invoke({
            "messages": [user_input]
        })

        print("Output:", result["messages"][-1])