import chromadb

client = chromadb.PersistentClient(
  path="./data/chroma"
)

collection = client.get_or_create_collection(
  name="documents"
)

def add_chunks(
  document_id: str,
  chunks: list[str],
  embeddings: list[list[float]]
):
  ids = [
    f"{document_id}_chunk_{index}"
    for index in range(len(chunks))
  ]

  metadatas = [
    {
      "document_id": document_id,
      "chunk_index": index
    }
    for index in range(len(chunks))
  ]

  collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
  )

  return ids

def search_chunks(
  query_embedding: list[float],
  top_k: int = 5
):
  results = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k
  )

  return results