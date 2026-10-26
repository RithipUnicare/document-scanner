from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from config.database import async_db_create, get_async_session
from models.DatabaseRegistry import registry

#Load environmental variables on root itself
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_db_create()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def main():
    return {"message": "Hello World"}
