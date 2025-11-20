import math
from typing import List, TypedDict, final

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """
    simple node that adds a greeting  message to the state
    """
    state["message"] = "hello " + state["message"] + " how is your day going?"
    return print(state)


graph = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")
app = graph.compile()
result = app.invoke({"message": "bob"})


def exercise_1(state: AgentState) -> AgentState:
    state["message"] = (
        state["message"] + "," + " you`re doing an amazing job learning LangGraph"
    )

    return state


graph_1 = StateGraph(AgentState)
graph_1.add_node("exercise_1", exercise_1)
graph_1.set_entry_point("exercise_1")
graph_1.set_finish_point("exercise_1")
app = graph.compile()
res = app.invoke({"message": "Maksym"})
