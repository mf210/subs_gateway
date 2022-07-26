import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient



class Segment(BaseModel):
    primary_language: str
    primary_subtitle: str | None = None
    secondary_subtitle: str | None = None
    secondary_language: str | None = None
    is_primary_closed_caption: bool | None = None
    is_secondary_closed_caption: bool | None = None
    phonetic_type: str | None = None
    movie_id: str | None = None
    movie_name: str | None = None
    user_language: str | None = None

app = FastAPI(docs_url="/translations/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(
        f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PWD']}@mongo", 27017)
    app.segment_collection = app.mongodb_client.subdb.segment

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.post('/storesegmentsub')
async def save_segmentsub(segmentsub: Segment):
    app.segment_collection.insert_one(segmentsub.dict())
    return {}

