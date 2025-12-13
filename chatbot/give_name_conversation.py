from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph ,START ,END
from typing import TypedDict
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class provide_structure(BaseModel):
    message: str = Field(description="The description of chat for which name is to be generated in two to 3 words")

from dotenv import load_dotenv

load_dotenv()   

# model = ChatOpenAI()
model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

structure_model = model.with_structured_output(provide_structure)


class graph_state(TypedDict):
    message: str
    
def getName(state:graph_state):
    question = state['message']
    prompt = f"Sugest a name of chat based on this description: {question}"
    res  = model.invoke([HumanMessage(content=prompt)])
    return {'message':res.content}
    
graph = StateGraph(graph_state)

graph.add_node('getName',getName)

graph.add_edge(START,'getName')
graph.add_edge('getName',END)
chatNameResponse = graph.compile()

# res = chatNameResponse.invoke({'message':HumanMessage(content="I want a chat bot that can help me plan my trips and suggest places to visit based on my interests.")})
# print(res)
