from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_answer
from app.services.vector_service import search_chunks

router = APIRouter(
  prefix="/chat",
  tags=["Chat"]
)

class ChatRequest(BaseModel):
  question: str
  top_k: int = 5
  document_id: str | None = None


@router.post("")
async def chat(request: ChatRequest):

  query_embedding = generate_embedding(
    request.question
  )

  results = search_chunks(
    query_embedding=query_embedding,
    top_k=request.top_k,
    document_id=request.document_id
  )

  sources = []

  documents = results.get("documents", [[]])[0]
  metadatas = results.get("metadatas", [[]])[0]
  distances = results.get("distances", [[]])[0]
  ids = results.get("ids", [[]])[0]

  for index, document in enumerate(documents):
    sources.append({
      "chunk_id": ids[index],
      "text": document,
      "metadata": metadatas[index],
      "distance": distances[index]
    })

  context = "\n\n".join(documents)

  answer = generate_answer(
    question=request.question,
    context=context
  )

  return {
    "question": request.question,
    "answer": answer,
    "sources": sources
  }