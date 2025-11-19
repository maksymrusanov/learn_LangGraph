import math
from typing import List, TypedDict

from langgraph.graph import StateGraph, state


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


class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    state["result"] = f'Hi there {state["name"]}! your sum {sum(state["values"])}'
    return state


graph_2 = StateGraph(AgentState)
graph_2.add_node("graph_2", process_values)
graph_2.set_entry_point("graph_2")
graph_2.set_finish_point("graph_2")
app = graph_2.compile()
res = app.invoke({"values": [1, 2, 3], "name": "Maksym"})
print(res)


class AgentState(TypedDict):
    name: str
    values: List[int]
    operation: str
    result: str


def exercise_2(state: AgentState) -> AgentState:
    if state["operation"] == "+":
        state["result"] = f"Hi {state['name']} your answer is {sum(state['values'])}"
    elif state["operation"] == "*":
        state["result"] = (
            f"Hi {state['name']} your answer is {math.prod(state['values'])}"
        )
    else:
        state["result"] = "Invalid"
    return state


graph_3 = StateGraph(AgentState)
graph_3.add_node("graph_3", exercise_2)
graph_3.set_entry_point("graph_3")
graph_3.set_finish_point("graph_3")
app_1 = graph_3.compile()
res_2 = app_1.invoke({"values": [1, 2, 3, 4], "name": "exercise_2", "operation": "+"})
print(res_2)
