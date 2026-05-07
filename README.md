# DocQueryAI Backend API

AI-powered FastAPI backend for chatting with documents using Retrieval-Augmented Generation (RAG). Upload PDFs, store embeddings in Qdrant, and generate contextual AI responses using Google Gemini. The API supports authentication, chat management, document storage, and semantic search. 

---

# 🚀 Features

* 🔐 JWT Authentication
* 📄 Upload & manage documents
* 💬 Chat with uploaded documents
* 🧠 RAG (Retrieval-Augmented Generation)
* 🔍 Semantic vector search
* ⚡ FastAPI backend architecture
* 📚 LangChain integration
* 🤖 Google Gemini AI integration
* 🗂️ Qdrant vector database
* 📑 Pagination support for chats/messages

---

# 🛠️ Tech Stack

## Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic

## AI / RAG

* LangChain
* Google Gemini
* HuggingFace Embeddings

## Database

* Qdrant Vector Database
* SQLite / PostgreSQL

---

# 📂 Project Structure

```bash
DocQueryAI/
│
├── routers/                # API routes
├── services/               # Business logic
├── models/                 # Database models
├── database/               # DB configuration
├── utils/                  # Helper functions
├── uploads/                # Uploaded PDFs
├── main.py                 # FastAPI entry point
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Nikhi111/DocQueryAI.git
cd DocQueryAI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GOOGLE_API_KEY=your_google_api_key
QDRANT_URL=http://localhost:6333
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🧠 Run Qdrant

Using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

# ▶️ Run Application

```bash
uvicorn main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

# 📘 API Documentation

FastAPI automatically generates Swagger documentation.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# 🔄 How It Works

1. User registers and logs in
2. JWT token is generated
3. User creates chat sessions
4. PDFs/documents are uploaded
5. Text is extracted and chunked
6. Embeddings are generated
7. Embeddings are stored in Qdrant
8. User asks questions
9. Relevant chunks are retrieved
10. Gemini generates contextual responses

---

# 📡 API Endpoints

Based on the exported OpenAPI schema. 

---

# 🔐 Authentication APIs

## Register User

```http
POST /auth/register
```

### Request Body

```json
{
  "name": "Nikhil",
  "email": "nikhil@example.com",
  "password": "password"
}
```

---

## Login User

```http
POST /auth/login
```

### Request Body

```json
{
  "email": "nikhil@example.com",
  "password": "password"
}
```

---

# 💬 Chat APIs

## Create Chat

```http
POST /user/create
```

### Request Body

```json
{
  "name": "AI Chat",
  "description": "Document discussion"
}
```

---

## Rename Chat

```http
PUT /user/{chat_id}/{name}
```

---

## Get All Chats

```http
GET /user/chats
```

---

## Send Message

```http
POST /user/chat/{chat_id}/message?message=Hello
```

---

## Get Chat Messages

```http
GET /user/chat/messages
```

### Query Parameters

| Parameter | Type    | Description       |
| --------- | ------- | ----------------- |
| chat_id   | integer | Chat ID           |
| cursor    | integer | Pagination cursor |
| limit     | integer | Max 50            |

---

# 📄 Document APIs

## Upload Document

```http
POST /user/documet/{chat_id}
```

### Request Body

```json
{
  "fileName": "sample.pdf",
  "filePath": "/uploads/sample.pdf"
}
```

---

## Get Documents

```http
GET /user/documets/{chat_id}
```

### Query Parameters

| Parameter | Type    | Description       |
| --------- | ------- | ----------------- |
| cursor    | integer | Pagination cursor |
| limit     | integer | Pagination limit  |

---

# 🧠 AI Pipeline

## Document Processing

* PDF loading
* Text extraction
* Chunk splitting
* Embedding generation

## Retrieval

* Semantic similarity search
* Vector matching using Qdrant

## Response Generation

* Context retrieval
* Gemini AI response generation

---

# 🔮 Future Improvements

* Streaming AI responses
* Multi-document querying
* OCR support
* File upload endpoint
* Role-based access
* Docker deployment
* Cloud storage integration
* WebSocket support

---

# 🤝 Contributing

1. Fork repository
2. Create feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Added feature"
```

4. Push branch

```bash
git push origin feature/new-feature
```

5. Open Pull Request

---



---

# 👨‍💻 Author

Developed by **Nikhil Shinde**

Repository:

[DocQueryAI GitHub Repository](https://github.com/Nikhi111/DocQueryAI?utm_source=chatgpt.com)
