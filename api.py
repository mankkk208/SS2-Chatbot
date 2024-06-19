from abc import ABC
from typing import Optional

from dotenv import load_dotenv
from os import getenv

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

from langchain_chroma import Chroma

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# FastAPI
app = FastAPI(
    title="LangChain API",
    debug=True
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context.\n\n<context>{context}</context>"),
    ("human", "{input}")
])

# Data model
class User(BaseModel):
    username: str
    password: str

class TrainData(BaseModel):
    text: str

class Message(BaseModel):
    text: str
    chat_id: Optional[str] = None
    
# Bot class
class BotAbstract(ABC):
    model = None
    embedding = None
    vector_store = None
    
    async def add_data(self, message: TrainData):
        await self.vector_store.aadd_texts([message.text])

    async def chat(self, message: Message):
        retriever = self.vector_store.as_retriever()
        chain = create_retrieval_chain(retriever, create_stuff_documents_chain(self.model, prompt))
        return await chain.ainvoke({
            "input": message.text
        })
    
    
class OpenAIBot(BotAbstract):
    def __init__(self):
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        # Lưu ý: để khởi tạo được instance thì api key cần có sẵn trong biến môi trường OPENAI_API_KEY
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.embedding = OpenAIEmbeddings("text-embedding-3-small")
        self.vector_store = Chroma(
            collection_name="openai",
            embedding_function=self.embedding,
            persist_directory="databases/"
        )


class GoogleAIBot(BotAbstract):
    def __init__(self):
        from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
        # Lưu ý: để khởi tạo được instance thì api key cần có sẵn trong biến môi trường GOOGLE_API_KEY
        self.model = GoogleGenerativeAI(model="gemini-pro")
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = Chroma(
            collection_name="google",
            embedding_function=self.embedding,
            persist_directory="databases/"
        )

# Create bot instance
bot: BotAbstract = None

if getenv("GOOGLE_API_KEY") is not None: 
    print("Using Google model")
    bot = GoogleAIBot()
elif getenv("OPENAI_API_KEY") is not None:
    print("Using OpenAI model")
    bot = OpenAIBot()
else: 
    raise RuntimeError("Environment variables is not properly configured")


# Authentication
fake_admin = {"username": "admin", "password": "admin"}

def verify_token(token: str = Depends(oauth2_scheme)):
    if token == "fake-token":
        return fake_admin
    raise HTTPException(401)



# API Endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == fake_admin["username"] and form_data.password == fake_admin["password"]:
        return {
            "status": "success",
            "access_token": "Bearer fake-token"
        }
    else: raise HTTPException(401)



@app.post("/add_data", dependencies=[Depends(verify_token)])
async def add_data(message: TrainData):
    try:
        await bot.add_data(message)
        return {"status": "success"}
    except Exception as e:
        print(repr(e))
        raise HTTPException(500)
        

@app.post("/chat")
async def chat(message: Message):
    try:
        result = await bot.chat(message)
        return {
            "status": "success",
            "response": result["answer"]
        }
        
    except Exception as e:
        print(repr(e))
        raise HTTPException(500)