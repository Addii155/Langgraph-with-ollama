from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()

model = ChatOpenAI()

res = model.invoke([HumanMessage(content='Hello from OpenAI model')])

print(res.content)