from fastapi import APIRouter
from pydantic import BaseModel

from app.core.response import success_response
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
  max_distance: float = 0.50

@router.post("")
async def chat(request: ChatRequest):

  query_embedding = generate_embedding(
    request.question
  )

  results = search_chunks(
    query_embedding=query_embedding,
    top_k=request.top_k,
    document_id=request.document_id,
    max_distance=request.max_distance
  )

  if not results:
    return success_response(
      message="AI generated answer successfully",
      data={
        "question": request.question,
        "answer": (
          "The answer is not available in the provided documents."
        ),
        "sources": [],
        "retrieval": {
          "requested_top_k": request.top_k,
          "returned_chunks": 0
        }
      }
    )

  context = "\n\n".join(
    result["document"]
    for result in results
  )

  answer = generate_answer(
    question=request.question,
    context=context
  )

  sources = [
    {
      "chunk_id": result["id"],
      "text": result["document"],
      "metadata": result["metadata"],
      "distance": result["distance"]
    }
    for result in results
  ]  

  return success_response(
    message = "AI generated answer successfully",
    data = {
      "question": request.question,
      "answer": answer,
      "sources": sources,
      "retrieval": {
        "requested_top_k": request.top_k,
        "returned_chunks": len(results)
      }
    }      
 )