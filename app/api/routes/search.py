from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_chunks

router = APIRouter(
  prefix="/search",
  tags=["Search"]
)

class SearchRequest(BaseModel):
  query: str
  top_k: int = 5

@router.post("")
async def search_documents(request: SearchRequest):

  query_embedding = generate_embedding(
    request.query
  )

  results = search_chunks(
    query_embedding=query_embedding,
    top_k=request.top_k
  )

  return results