from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

from apps.todo.routers import router as todo_router

load_dotenv()

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.getenv('DB_URL'))
    app.mongodb = app.mongodb_client[os.getenv('DB_NAME')]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(todo_router)
