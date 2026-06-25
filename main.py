from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.groups import router as groups_router
from app.routers.matches import router as matches_router
from app.routers.predictions import router as predictions_router
from app.routers.teams import router as teams_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

##core
from app.core.database import Base
from app.core.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()
# corss
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://pollapp-front.vercel.app",
        "https://www.pollapp.xyz",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(matches_router)
app.include_router(predictions_router)
app.include_router(teams_router)

@app.get("/")
def health_check():
    return {
        "message": "API running"
    }
