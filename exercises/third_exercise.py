import math
from typing import List, TypedDict, final

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: int
    skils: list[str]
    final: str


def node_1(state: AgentState) -> AgentState:
    state["final"] = f"Hi {state["name"]}"
    return state


def node_2(state: AgentState) -> AgentState:
    state["final"] = state["final"] + f" You are {state["age"]}"
    return state


def node_3(state: AgentState) -> AgentState:
    state["final"] = state["final"] + f" you have skills in:{", ".join(state["skils"])}"
    return state


graph = StateGraph(AgentState)
graph.add_node("first_node", node_1)
graph.add_node("second_node", node_2)
graph.add_node("third_node", node_3)


graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")
app = graph.compile()
res_3 = app.invoke({"name": "w", "age": 22, "skils": ["q", "w", "e"]})
print(res_3.state)
