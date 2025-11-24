from langchain_core import messages
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
import os
from langgraph import graph
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


llm = ChatOpenAI(model="gpt-4o")


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append((AIMessage(content=response.content)))

    print(f"\nAI:{response.content}")
    print("CURRENT STATE: ", state["messages"])
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()
conversation_history = []
user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke(({"messages": conversation_history}))
    conversation_history = result["messages"]
    user_input = input("Enter: ")
with open("logging.txt", "w") as file:
    file.write("Your logs:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"you :{message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI:{message.content}\n\n")
    file.write("end")
print("conversation saved ")
