from langgraph.graph import StateGraph ,START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.checkpoint.memory import MemorySaver;
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv


load_dotenv()



from IPython.display import Image

model = ChatOpenAI()

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

res = workflow.invoke({'message':[HumanMessage(content='Hello')]},config=config)

print(res)
history = workflow.get_state(config={'configurable':{'thread_id':'thread-1'}}).values['message']
for i in history:
    print(i.content) 
