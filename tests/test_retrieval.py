from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_chunks

def test_retrieval():

  question = "How many annual leave days do employees receive?"

  query_embedding = generate_embedding(question)

  results = search_chunks(
    query_embedding=query_embedding,
    top_k=5
  )

  assert len(results) > 0

  retrieved_text = " ".join(
    result["document"]
    for result in results
  ).lower()

  assert "20" in retrieved_text