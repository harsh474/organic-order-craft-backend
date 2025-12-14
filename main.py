from fastapi import FastAPI
from app.config.settings import settings
from app.routers import auth
from app.core.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.models import *   # 🔥 THIS IS THE KEY

origins = [
     "http://localhost:8080"
]

app = FastAPI(title=settings.APP_NAME)

# Properly configure CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # list of allowed origins, or ["http://localhost:8080"]
    allow_credentials=True,         # set to True if frontend sends cookies / Authorization via fetch with credentials
    allow_methods=["*"],            # allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],            # allow all headers
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)

@app.get("/", tags=["home"])
def home():
    return {"message": "Welcome to the Ghee E-Commerce Backend API"}

# Routers will be included here in the next steps.
