from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 
from vector import retriever
from pydantic import BaseModel, Field

class ReviewAnswer(BaseModel):
    reviews: str = Field(..., description="List of reviews retrieved from the vector store")
    questions: str = Field(..., description="The question about the reviews")

model = OllamaLLM(model="llama2", temperature=0.7)

template = """
You are a expert in answering review about pizza restaurants.
here are some reviews:{reviews}
here are some questions about the reviews:{questions}

"""

prompt = ChatPromptTemplate.from_template(template)

chat  = prompt | model 

while True:
    print("--------------------")
    question = input("ask a question about pizza restaurants reviews: ")
    if question == 'q':
        break
    review = retriever.invoke(question)
    for data in review:
        print("--------------------")
        print(data.page_content)
        print(data.metadata)
        print(end="--------------------\n")
    print(end="--------------------\n")
    result = chat.invoke({"reviews":review,"questions":question})
    print(result)
    
