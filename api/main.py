from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from langchain import LangChain
from langchain.vectorstores import MongoDBVectorStore

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot
vector_store = MongoDBVectorStore(db)

# Mock admin user
fake_admin = {"username": "admin", "password": "admin"}

class User(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    text: str

def verify_token(token: str):
    if token == "fake-token":
        return fake_admin
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == fake_admin["username"] and form_data.password == fake_admin["password"]:
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/admin/add_data", dependencies=[Depends(verify_token)])
async def add_data(message: Message):
    vector_store.add_text(message.text)
    return {"status": "success"}

@app.get("/chat")
async def chat(message: Message):
    response = LangChain(vector_store).ask(message.text)
    return {"response": response}
