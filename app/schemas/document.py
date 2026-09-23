from pydantic import BaseModel

class DocumentUploadData(BaseModel):
  document_id: str
  filename: str
  content_type: str
  size: int
  chunk_count: int
  embedding_dimensions: int
  status: str

class DocumentResponse(BaseModel):
  success: bool
  message: str
  data: DocumentUploadData