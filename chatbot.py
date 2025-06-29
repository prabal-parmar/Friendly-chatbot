from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages, Sequence


load_dotenv()

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a friendly helpful AI Chatbot and you talk with user in {language} langugae. User's name is {name}."),
    HumanMessagePromptTemplate.from_template("User will talk friendly to Chatbot"),
    MessagesPlaceholder(variable_name="messages")
])


llm = ChatGroq(temperature=0, model='llama3-8b-8192')

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str
    name: str


def model(state: State):
    msg = prompt_template.invoke({"messages": state['messages'], "language": state['language'], "name": state["name"]})
    response = llm.invoke(msg)
    return {"messages": [response]}

graph = StateGraph(state_schema=State)

graph.add_edge(START, "model")
graph.add_node("model", model)

memory = MemorySaver()
# Send response to app.py
def send_answer(user_id: str, query: str, language: str, name: str):

    app = graph.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": user_id}}
    input_msg = [HumanMessage(query)]
    output = app.invoke({"messages": input_msg, "language": language, "name": name}, config)

    return output["messages"][-1].content