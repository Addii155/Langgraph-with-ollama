from langgraph.graph import StateGraph ,START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver;
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import tools_condition,ToolNode
import sqlite3
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests

load_dotenv()

#  LLM 
model = ChatOpenAI()

#  Tools 

search_tool = DuckDuckGoSearchRun()

@tool
def get_stock_price(symbol:str):
    """"Get the current stock price for a given symbol.(e.g, 'AAPL' for Apple Inc. , 'TSLA' for Tesla Inc.)"""
    STOCK_API_KEY = load_dotenv()
    query_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={STOCK_API_KEY}'
    res = requests.get(query_url)
    print(res.json())

tools = [search_tool,get_stock_price]


llm_with_tools = model.bind_tools(tools)


connection= sqlite3.connect('chatbot.db',check_same_thread=False)


class chatbot_state(TypedDict):
    
    message: Annotated[list[BaseMessage],add_messages]


def chatNode(state:chatbot_state):
    
    question =  state['message']
    res  = llm_with_tools.invoke(question)
    return {'message':[res]}

chatbot= StateGraph(chatbot_state)

tool_node= ToolNode(tools)

chatbot.add_node("chatNode", chatNode)
chatbot.add_node("tools", tool_node)

chatbot.add_edge(START,"chatNode")
chatbot.add_conditional_edges("chatNode",tools_condition)
# chatbot.add_edge("tools",END)
chatbot.add_edge("chatNode",END)

checkPointer = SqliteSaver(conn=connection)

workflow = chatbot.compile(checkpointer=checkPointer)

# config = {'configurable':{'thread_id':'thread-1'}}

# res = workflow.invoke({'message':[HumanMessage(content='Hello')]},config=config)

# print(res)
# history = workflow.get_state(config={'configurable':{'thread_id':'thread-1'}}).values['message']
# for i in history:
#     print(i.content) 


def get_all_thread_id():
    all_thread_id=set()
    for i in checkPointer.list(None):
        all_thread_id.add(i.config['configurable']['thread_id'])
    newlist = list(all_thread_id)
    return newlist
    
# print(get_all_thread_id())

# print(workflow.get_state(config={'configurable':{'thread_id':'8e21f755-e2f7-449a-937f-18a75786d793'}}).values)