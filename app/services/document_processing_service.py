from app.db.mongo import documents_collection
from app.services.vector_service import add_chunks

def update_document_status(
  document_id: str,
  status: str,
  **extra_fields
):
  documents_collection.update_one(
    {
      "document_id": document_id
    },
    {
      "$set": {
        "status": status,
        **extra_fields
      }
    }
  )