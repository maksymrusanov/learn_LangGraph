from typing import TypedDict
from langgraph.graph import END, START, StateGraph


## Conditional graph
class AgentState(TypedDict):
    number_1: int
    operation: str
    number_2: int
    finalNumber: int


def adder(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number_1"] + state["number_2"]
    return state


def subtractor(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number_1"] - state["number_2"]
    return state


def decide_next_node(state: AgentState) -> AgentState:
    if state["operation"] == "+":
        return "addition_operation"

    elif state["operation"] == "-":
        return "subtraction_operation"


graph = StateGraph(AgentState)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("router", lambda state: state)
graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {  ## Edge:Node
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node",
    },
)

graph.add_edge("add_node", END)

graph.add_edge("subtract_node", END)


app = graph.compile()
q = AgentState(number_1=10, operation="-", number_2=5)
print(app.invoke(q))


##execrise
class AgentState1(TypedDict):
    number1: int
    operation1: str
    number2: int
    final_number: int
    number3: int
    operation2: str
    number4: int
    final_number2: int


def add_node1(state: AgentState1):
    state["final_number"] = state["number1"] + state["number2"]
    return state


def subtract_node1(state: AgentState1):
    state["final_number"] = state["number1"] - state["number2"]
    return state


def decide_next_node1(state: AgentState1):
    if state["operation1"] == "+":
        return "adding_operation1"
    elif state["operation1"] == "-":
        return "subtraction_operation1"


def add_node2(state: AgentState1):
    state["final_number2"] = state["number3"] + state["number4"]
    return state


def subtract_node2(state: AgentState1):
    state["final_number2"] = state["number1"] - state["number4"]
    return state


def decide_next_node2(state: AgentState1):
    if state["operation2"] == "+":
        return "adding_operation2"
    elif state["operation2"] == "-":
        return "subtraction_operation2"


graph = StateGraph(AgentState1)
graph.add_node("add_node1", add_node1)
graph.add_node("subtract_node1", subtract_node1)
graph.add_node("add_node2", add_node2)
graph.add_node("subtract_node2", subtract_node2)
graph.add_node("router1", lambda state: state)
graph.add_node("router2", lambda state: state)
graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1",
    decide_next_node1,
    {  ## Edge:Node
        "adding_operation1": "add_node1",
        "subtraction_operation1": "subtract_node1",
    },
)
graph.add_edge("add_node1", "router2")
graph.add_edge("subtract_node1", "router2")

graph.add_conditional_edges(
    "router2",
    decide_next_node2,
    {"adding_operation2": "add_node2", "subtraction_operation2": "subtract_node2"},
)
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)
app1 = graph.compile()
w = AgentState1(
    number1=10,
    operation1="-",
    number2=5,
    number3=7,
    number4=2,
    operation2="+",
)
print(app1.invoke(w))
