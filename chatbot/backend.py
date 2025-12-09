from langgraph.graph import StateGraph ,START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage 
from langgraph.checkpoint.memory import MemorySaver;
from typing import TypedDict,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv


load_dotenv()



from IPython.display import Image

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
)

class chatbot_state(TypedDict):
    
    message: Annotated[list[BaseMessage],add_messages]


def chatNode(state:chatbot_state):
    
    question =  state['message']
    res  = model.invoke(question)
    return {'message':[res]}

chatbot= StateGraph(chatbot_state)

chatbot.add_node('chatNode', chatNode)

chatbot.add_edge(START,'chatNode')
chatbot.add_edge('chatNode',END)

checkPointer = MemorySaver()

workflow = chatbot.compile(checkpointer=checkPointer)

config = {'configurable':{'thread_id':'thread-1'}}



