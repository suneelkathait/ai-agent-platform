import chromadb

client = chromadb.PersistentClient(
  path="./data/chroma"
)

collection = client.get_or_create_collection(
  name="documents"
)

def delete_document_chunks(document_id: str):
  collection.delete(
    where={
      "document_id": document_id
    }
  )

def add_chunks(
  document_id: str,
  filename: str,
  content_type: str | None,
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
      "filename": filename,
      "content_type": content_type or "",
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
  top_k: int = 5,
  document_id: str | None = None,
  max_distance: float = 1
):
  query_kwargs = {
    "query_embeddings": [query_embedding],
    "n_results": top_k
  }

  if document_id:
    query_kwargs["where"] = {
      "document_id": document_id
    }

  results = collection.query(**query_kwargs)

  documents = results.get("documents", [[]])[0]
  metadatas = results.get("metadatas", [[]])[0]
  distances = results.get("distances", [[]])[0]
  ids = results.get("ids", [[]])[0]

  filtered_results = []

  for index, distance in enumerate(distances):
    if distance <= max_distance:
      filtered_results.append({
        "id": ids[index],
        "document": documents[index],
        "metadata": metadatas[index],
        "distance": distance
      })

  return filtered_results
