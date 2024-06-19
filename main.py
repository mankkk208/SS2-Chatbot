if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
    exit()

import api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import webbrowser

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Application startup")
    webbrowser.open("http://localhost:8000/chat.html")
    yield

app = FastAPI(
    title="Chatbot",
    debug=True,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# API endpoint
app.mount("/api", api.app)

# Static endpoint
app.mount("/", StaticFiles(directory="static"))