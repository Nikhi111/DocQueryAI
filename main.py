from dotenv import load_dotenv
from qdrant_client.http.models import VectorParams, Distance
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database.DbConnect import engine
from models import modelDb
from controller import auth, chat,resourceControlller
from qdrant_client import QdrantClient

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# create tables
modelDb.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome sir"
@app.on_event("startup")
def init_qdrant():
    client = QdrantClient(url="http://localhost:6333")
    if not client.collection_exists(collection_name="DocQueryAi"):
        print("Creating collection...")
        client.create_collection(
            collection_name="DocQueryAi",
            vectors_config=VectorParams(
                size=384,
                # change based on your embedding model
                distance=Distance.COSINE
            )
        )
    else:
        print("Collection already exists ✅")
# include routers

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(resourceControlller.router)