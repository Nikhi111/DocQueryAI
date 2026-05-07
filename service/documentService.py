import tempfile
import uuid
from xml.dom.minidom import Document

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from langchain_community.embeddings import HuggingFaceEmbeddings

import requests
from models.modelDb import DocumentDB
from models.models import DocumentValidator
from sqlalchemy.orm import Session


def load_pdf_from_url(url):
    response = requests.get(url)
    print("STATUS:", response.status_code)
    print("URL:", url)
    if response.status_code != 200:
        raise Exception("Failed to download file")

    # save temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()

    loader = PyPDFLoader(temp_file.name)
    return loader.load()


def addDocument(ufilename: str, ufilepath: str, chat_id: int, user_id: int, db: Session):
    newDoc = DocumentDB(
        chat_id=chat_id,
        user_id=user_id,
        filePath=ufilepath,
        fileName=ufilename
    )
    db.add(newDoc)
    db.commit()
    db.refresh(newDoc)
    return newDoc


def documentEmbedding(filepath: str, chat_id, user_id, document_id):
    client = QdrantClient(url="http://localhost:6333")
    docs = load_pdf_from_url(filepath)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    # DIAGNOSTIC: Print chunk count
    print(f"DEBUG: Created {len(chunks)} chunks")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [chunk.page_content for chunk in chunks]

    # DIAGNOSTIC: Print texts count
    print(f"DEBUG: Prepared {len(texts)} texts for embedding")

    # DIAGNOSTIC: Catch embedding errors
    try:
        vectors = embedding_model.embed_documents(texts)
        print(f"DEBUG: Generated {len(vectors)} vectors")

        # DIAGNOSTIC: Check vector dimensions
        if vectors:
            print(f"DEBUG: First vector dimension: {len(vectors[0])}")
    except Exception as e:
        print(f"ERROR: Embedding failed - {e}")
        raise

    # DIAGNOSTIC: Verify vectors match chunks
    if len(vectors) != len(chunks):
        print(f"WARNING: Mismatch! {len(chunks)} chunks but {len(vectors)} vectors")

    # Build points with proper structure
    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,

            payload={
                "text": chunk.page_content,
                "chat_id": chat_id,
                "user_id": user_id,
                "document_id": document_id,
                "chunk_index": i
            }
        )
        points.append(point)

        # DIAGNOSTIC: Print every 5th point
        if i % 5 == 0:
            print(f"DEBUG: Created point {i + 1}/{len(chunks)}")

    print(f"DEBUG: Total points created: {len(points)}")

    # DIAGNOSTIC: Add error handling for upsert
    try:
        client.upsert(
            collection_name="DocQueryAi",
            points=points
        )
        print(f"SUCCESS: Upserted {len(points)} points to Qdrant")
    except Exception as e:
        print(f"ERROR: Upsert failed - {e}")
        raise

    print("Docs:", len(docs))
    print("points:", len(points))
    print("Chunks:", len(chunks))

    return {
        "success": True,
        "docs_count": len(docs),
        "chunks_count": len(chunks),
        "points_count": len(points)
    }