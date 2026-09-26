from datetime import datetime, timezone

from app.db.mongo import documents_collection
from app.services.document_service import update_document_status
from app.services.document_service import extract_document_text
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import add_chunks

def process_document(
  document_id: str,
  filename: str,
  content_type: str | None,
  file_content: bytes,
  file_size: int,
):
  try:
    # -----------------------------------
    # 1. Mark document as processing
    # -----------------------------------

    update_document_status(
      document_id=document_id,
      status="processing"
    )

    # -----------------------------------
    # 2. Extract text
    # -----------------------------------

    extracted_text = extract_document_text(
      filename,
      file_content
    )

    if not extracted_text.strip():
      raise ValueError(
        "No text could be extracted from the document"
      )

    # Store extracted text in MongoDB
    documents_collection.update_one(
      {
        "document_id": document_id
      },
      {
        "$set": {
          "extracted_text": extracted_text,
          "updated_at": datetime.now(timezone.utc)
        }
      }
    )

    # -----------------------------------
    # 3. Create chunks
    # -----------------------------------

    chunks = chunk_text(
      extracted_text,
      chunk_size=100,
      chunk_overlap=20
    )

    if not chunks:
      raise ValueError(
        "No chunks were created from the document"
      )

    # -----------------------------------
    # 4. Generate embeddings
    # -----------------------------------

    embeddings = generate_embeddings(chunks)

    if not embeddings:
      raise ValueError(
        "No embeddings were generated"
      )

    embedding_dimensions = len(embeddings[0])

    # -----------------------------------
    # 5. Store chunks + embeddings
    #    in ChromaDB
    # -----------------------------------

    add_chunks(
      document_id=document_id,
      filename=filename,
      content_type=content_type,
      chunks=chunks,
      embeddings=embeddings
    )

    # -----------------------------------
    # 6. Mark document as completed
    # -----------------------------------

    documents_collection.update_one(
      {
        "document_id": document_id
      },
      {
        "$set": {
          "status": "completed",
          "chunk_count": len(chunks),
          "embedding_dimensions": embedding_dimensions,
          "updated_at": datetime.now(timezone.utc),
          "error": None
        }
      }
    )

  except Exception as error:

    # -----------------------------------
    # 7. Mark document as failed
    # -----------------------------------

    documents_collection.update_one(
      {
        "document_id": document_id
      },
      {
        "$set": {
          "status": "failed",
          "error": str(error),
          "updated_at": datetime.now(timezone.utc)
        }
      }
    )

    raise ValueError(
      "Document processing failed: " + str(error)
    )