import math
from typing import List, TypedDict, final

from langgraph.graph import StateGraph


##multiply input graph
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
