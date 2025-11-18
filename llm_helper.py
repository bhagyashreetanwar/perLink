from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=MODEL_NAME)


if __name__ == "__main__":
    response = llm.invoke("Two most important ingradient in samosa are ")
    print(response.content)



