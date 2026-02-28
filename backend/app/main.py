from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.db.init_db import init_db
from app.db.seed import seed_sql

app = FastAPI(title="Systex Mini Hybrid-RAG Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.on_event("startup")
def _startup():
    init_db()
    seed_sql()

app.include_router(chat_router)