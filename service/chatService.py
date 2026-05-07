from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from models.modelDb import MessageDB
from models.models import Message
from sqlalchemy.orm import Session
from langchain_qdrant import QdrantVectorStore


def getLlmResult(message: str, user_id, chat_id):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print(f"--- Debug: Connecting to Qdrant collection 'DocQueryAi' ---")

    vectordb = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="DocQueryAi"
    )

    client = vectordb.client  # 🔥 IMPORTANT

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    print(f"--- Debug: Searching for message: '{message}' ---")
    print(f"--- Debug: Applying filters -> user_id: {user_id}, chat_id: {chat_id} ---")

    # 🔥 RAW QDRANT SEARCH (THIS FIXES YOUR ISSUE)
    results = client.query_points(
        collection_name="DocQueryAi",
        query=embedding_model.embed_query(message),  # 🔥 changed param name
        limit=10,
        with_payload=True,
        query_filter={
            "must": [
                {"key": "chat_id", "match": {"value": chat_id}},
                {"key": "user_id", "match": {"value": user_id}}
            ]
        }
    )

    points = results.points  # 🔥 IMPORTANT

    print(f"--- Debug: Found {len(points)} relevant document chunks ---")

    # Debug payload
    for i, r in enumerate(points):
        print(f"[Chunk {i + 1}] Payload keys: {list(r.payload.keys())}")
        print(f"Preview: {r.payload.get('text', '')[:150]}")
    # 🔥 BUILD CONTEXT CORRECTLY
    context_text = "\n\n".join([
        f"Chunk {r.payload.get('chunk_index')}: {r.payload.get('text', '')}"
        for r in points
    ])
    print(f"--- Debug: Context Length: {len(context_text)} characters ---")
    print(context_text[:500])

    system_prompt = f"""
    You are an AI assistant.

    Answer ONLY using the provided context.

    Rules:
    - Read ALL context carefully
    - If answer exists → give COMPLETE answer
    - If partially available → answer as much as possible
    - If answer truly not present → say "Not in document"

    CONTEXT:
    {context_text}
    """

    print(f"--- Debug: Sending request to Gemini... ---")

    response = llm.invoke([
        ("system", system_prompt),
        ("human", message)
    ])

    print(f"--- Debug: LLM Response Received ---")
    print(response.content)

    return response


def saveMessage(message:str,role:str,user_id,chat_id,db:Session):
    message=MessageDB(
        content=message,
        role=role,
        user_id=user_id,
        chat_id=chat_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return  message




