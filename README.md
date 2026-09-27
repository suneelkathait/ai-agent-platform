# AI Document Knowledge Platform

An AI-powered document knowledge platform built with **FastAPI, Python, Google Gemini, MongoDB, and ChromaDB**.

The platform allows users to upload documents such as **PDF and TXT files**, processes their content, creates searchable vector embeddings, and uses **Retrieval-Augmented Generation (RAG)** to answer questions based on the uploaded documents.

The main goal is to provide **grounded AI responses from the user's documents instead of relying only on the LLM's general knowledge**.

---

## 🚀 Project Overview

Traditional LLM applications can answer general questions, but they do not automatically know the private information contained inside a user's documents.

This project solves that problem using a **RAG pipeline**.

### Basic Flow

```text
User
  ↓
FastAPI API
  ↓
Document Upload
  ↓
PDF/TXT Text Extraction
  ↓
Text Chunking
  ↓
Embedding Generation
  ↓
ChromaDB
  ↓
User Question
  ↓
Similarity Search
  ↓
Relevant Document Chunks
  ↓
Google Gemini
  ↓
Grounded Answer + Sources
```

---

## 🎯 Problem This Project Solves

Suppose a user uploads:

* Company documentation
* Legal documents
* Technical documentation
* Policies
* Contracts
* Knowledge-base documents
* Internal TXT/PDF files

The user can then ask questions such as:

```text
"What is the termination clause?"

"What are the payment conditions?"

"What is the refund policy?"

"Summarize the responsibilities mentioned in this document."
```

Instead of sending the entire document to Gemini every time, the system:

1. Searches the vector database.
2. Finds the most relevant chunks.
3. Sends only those chunks as context to Gemini.
4. Generates an answer based on that context.

This makes the application more suitable for **large document collections and knowledge-based AI applications**.

---

# 🧠 Core Technology: RAG

This project implements **Retrieval-Augmented Generation (RAG)**.

RAG combines two major capabilities:

### Retrieval

Find relevant information from the user's documents.

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
```

### Generation

Use the retrieved information as context for the LLM.

```text
Question + Retrieved Context
             ↓
         Gemini LLM
             ↓
          Answer
```

The final response is therefore generated using information retrieved from the uploaded documents.

---

# 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │      Client      │
                    │ Postman / Frontend│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │      Routes      │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
       Document APIs                    Chat APIs
              │                             │
              ▼                             ▼
       Document Service               RAG Service
              │                             │
              ▼                             ▼
      Text Extraction                 ChromaDB
              │                       Vector Search
              ▼                             │
        Chunking                           ▼
              │                      Relevant Context
              ▼                             │
        Embeddings                          │
              │                             ▼
              └──────► ChromaDB ◄────── Gemini
                         │
                         │
                         ▼
                      MongoDB
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Pydantic Settings

## AI / LLM

* Google Gemini
* Embeddings
* Retrieval-Augmented Generation (RAG)

## Databases

### MongoDB

Used for application-level document metadata and document lifecycle information.

Examples:

* Document ID
* File name
* File type
* Processing status
* Upload information
* Document metadata

### ChromaDB

Used as the vector database.

It stores:

* Document chunks
* Embeddings
* Metadata
* Vector-search information

ChromaDB is responsible for semantic similarity search.

---

# 📄 Supported Documents

Supported:

* PDF
* TXT

The document processing pipeline is:

```text
File Upload
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
```

---

# ✂️ Document Chunking

Large documents are divided into smaller pieces called **chunks**.

For example:

```text
Original Document
        ↓
 ┌──────────────┐
 │ Chunk 1      │
 ├──────────────┤
 │ Chunk 2      │
 ├──────────────┤
 │ Chunk 3      │
 ├──────────────┤
 │ Chunk 4      │
 └──────────────┘
```

Each chunk is converted into an embedding and stored in ChromaDB.

Chunking allows the retrieval system to find only the relevant parts of a document.

---

# 🔎 Semantic Search

The application uses vector similarity search rather than relying only on exact keyword matching.

For example, if a document contains:

```text
"The agreement may be terminated by either party
with thirty days written notice."
```

A user can ask:

```text
"How can I cancel the agreement?"
```

Even though the exact word `"cancel"` may not exist in the document, semantic search can identify the relevant chunk because the meanings are similar.

---

# 🤖 Gemini Integration

Google Gemini is used as the **LLM generation layer**.

Gemini receives:

```text
User Question
+
Relevant Retrieved Context
```

and generates the final response.

The prompt instructs Gemini to use the provided document context rather than inventing information.

Conceptually:

```text
Question
   +
Retrieved Chunks
   ↓
Gemini
   ↓
Grounded Answer
```

---

# 🛡️ Hallucination Control

The application follows a context-grounded approach.

Gemini is instructed to answer using the retrieved document context.

If relevant information cannot be found, the system should avoid generating an unsupported answer.

The RAG pipeline also uses retrieval filtering so that irrelevant chunks are not blindly sent to Gemini.

---

# 🎯 Retrieval Filtering

The retrieval process uses:

* `top_k` results
* Similarity/distance filtering
* `document_id` metadata filtering

For example:

```text
User Question
      ↓
Vector Search
      ↓
Top K Chunks
      ↓
Distance Threshold
      ↓
Relevant Chunks
      ↓
Gemini
```

If no relevant chunks are found, the system can return a response without making an unnecessary Gemini request.

---

# 🗄️ Database Responsibilities

The project intentionally separates database responsibilities.

### MongoDB

MongoDB acts as the **application source of truth** for document information.

```text
MongoDB
 ├── document metadata
 ├── file information
 ├── processing status
 └── document lifecycle
```

### ChromaDB

ChromaDB handles the **semantic/vector search layer**.

```text
ChromaDB
 ├── chunks
 ├── embeddings
 ├── metadata
 └── similarity search
```

This separation keeps application data and vector-search data logically independent.

---

# 🔄 Document Processing Status

Document processing can happen asynchronously.

A document can move through states such as:

```text
uploaded
    ↓
processing
    ↓
completed
```

If processing fails:

```text
uploaded
    ↓
processing
    ↓
failed
```

FastAPI `BackgroundTasks` can be used so that document processing does not unnecessarily block the upload request.

---

# 📚 RAG Pipeline

The complete RAG pipeline is:

```text
1. Upload document
       ↓
2. Validate file
       ↓
3. Extract text
       ↓
4. Split text into chunks
       ↓
5. Generate embeddings
       ↓
6. Store chunks + embeddings
       ↓
7. User asks question
       ↓
8. Generate query embedding
       ↓
9. Search ChromaDB
       ↓
10. Filter relevant chunks
       ↓
11. Build Gemini prompt
       ↓
12. Generate answer
       ↓
13. Return answer + sources
```

---

# 🔌 API Overview

The project exposes APIs for document management and AI-powered querying.

Example endpoints:

```text
POST   /api/v1/documents/upload
GET    /api/v1/documents
GET    /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}

POST   /api/v1/chat
POST   /api/v1/chat/stream
```

The exact endpoint list may vary depending on the current implementation.

---

# 💬 Chat / Question Answering

The chat API follows this process:

```text
POST /chat
      ↓
Receive question
      ↓
Create query embedding
      ↓
Search ChromaDB
      ↓
Retrieve relevant chunks
      ↓
Build context
      ↓
Call Gemini
      ↓
Return answer
```

The response can include useful retrieval information such as:

* Answer
* Source document
* Relevant chunks
* Retrieval metadata

This helps make the AI response more transparent.

---

# ⚡ Streaming Responses

The project also supports a streaming chat approach using **Server-Sent Events (SSE)**.

Conceptually:

```text
User Question
     ↓
RAG Retrieval
     ↓
Gemini
     ↓
Token/Chunk Stream
     ↓
SSE
     ↓
Frontend
```

This allows the frontend to display the AI response progressively instead of waiting for the entire response.

---

# 🧹 Document Deletion

Deleting a document requires synchronization between the databases.

```text
DELETE Document
      │
      ├── MongoDB
      │
      └── ChromaDB
```

This prevents stale vector chunks from remaining searchable after the document has been deleted.

# ⚙️ Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key

MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=your_database_name

CHROMA_HOST=localhost
CHROMA_PORT=8000
```

---

# 🚀 Local Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment

Create:

```text
.env
```

and add the required environment variables.

## 5. Start Required Services

Start MongoDB and ChromaDB according to the project's Docker configuration.

For Docker Compose:

```bash
docker compose up -d
```

Check containers:

```bash
docker ps
```

## 6. Start FastAPI

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 🧪 Testing

API testing can be performed using:

* Swagger UI
* Postman
* Automated tests

Example workflow:

```text
1. Upload PDF/TXT
2. Check processing status
3. Ask question
4. Verify retrieved sources
5. Verify generated answer
6. Delete document
7. Verify document and vectors are removed
```

---

# 🧠 Concepts Covered

This project is designed to provide practical experience with:

### Backend

* Python
* FastAPI
* REST APIs
* Async programming
* Background tasks
* Pydantic
* Exception handling
* API validation

### AI

* LLM
* Google Gemini
* Prompt engineering
* Embeddings
* Vector databases
* Semantic search
* Retrieval-Augmented Generation
* Context grounding
* Hallucination control

### RAG

* Document ingestion
* Text extraction
* Text chunking
* Embedding generation
* Vector storage
* Similarity search
* Metadata filtering
* Retrieval thresholds
* Context construction
* Source attribution

### Database

* MongoDB
* ChromaDB
* Database separation
* Document lifecycle management
* Vector data management

### System Design

* Service-layer architecture
* Separation of responsibilities
* Asynchronous processing
* Streaming responses
* Database synchronization
* Scalable AI architecture

---

# 🎯 Project Goal

The goal of this project is to build a practical **AI-powered document knowledge system** that demonstrates how modern applications combine:

```text
FastAPI
   +
Document Processing
   +
Embeddings
   +
Vector Database
   +
RAG
   +
Gemini
   +
MongoDB
   +
Streaming
```

The project can serve as a foundation for building enterprise applications such as:

* Internal company knowledge assistants
* Legal document assistants
* Technical documentation assistants
* Policy assistants
* Contract analysis systems
* Customer support knowledge systems
* AI-powered enterprise search
