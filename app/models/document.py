from datetime import datetime, timezone

def create_document(
  document_id: str,
  filename: str,
  content_type: str | None,
  size: int
):
  return {
    "document_id": document_id,
    "filename": filename,
    "content_type": content_type,
    "size": size,
    "status": "uploaded",
    "chunk_count": 0,
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc),
    "error": None
  }