from dotenv import load_dotenv
from langchain_core import messages
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, message
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
document_content = ""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content: str) -> str:
    """
    updates document with content
    """
    global document_content
    document_content = content
    return f"document updated.Content is:\n{document_content}"


@tool
def save(filename: str) -> str:
    """save current document to a text filename
    Args:
        filename:Name for the text file
    """
    global document_content
    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"
    try:
        with open(filename, "w") as file:
            file.write(document_content)
        print("document save to: {filename}")
        return f"document saved to {filename}"
    except Exception as e:
        return f"error :{str(e)}"


tools = [update, save]
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)


def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    
    The current document content is:{document_content}
    """
    )
    if not state["messages"]:
        user_input = "i am ready to help you.What would you like to create?"
        user_message = HumanMessage(user_input)
    else:
        user_input = input("\nWhat would you like to do with document?")
        print(f"\nUSER:{user_input}")
        user_message = HumanMessage(user_input)
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = model.invoke(all_messages)
    print(f"\nAI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f'USING TOOLS:{[tc["name"] for tc in response.tool_calls]}')
    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    """
    Determine if we should continue  or end
    """
    messages = state["messages"]
    if not messages:
        return "continue"
    for messages in reversed(messages):
        if (
            isinstance(message, ToolMessage)
            and "saved" in message.content.lower()
            and "document" in message.content.lower()
        ):
            return "end"
    return "continue"


def print_messages(messages):
    if not messages:
        return
    for message in messages[-3]:
        if isinstance(message, ToolMessage):
            print(f"\nTOOL RESULT: {message.content}")
