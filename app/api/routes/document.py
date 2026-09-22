from uuid import uuid4
from fastapi import APIRouter, File, UploadFile

from app.services.document_service import extract_document_text
from app.core.exceptions import AppException
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import add_chunks

router = APIRouter(
  prefix="/documents",
  tags=["Documents"]
)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
  if not file.filename:
    raise AppException(
      error_code="REQUIRED_FIELDS",
      message="File name is required",
      status_code=400,
    )

  allowed_extensions = {".pdf", ".txt"}

  extension = "." + file.filename.lower().rsplit(".", 1)[-1]

  if extension not in allowed_extensions:
    raise AppException(
        error_code="UNSUPPORTED_FILE",
        message="Only PDF and TXT files are supported",
        status_code=400,
      )

  file_content = await file.read()

  if not file_content:
    raise AppException(
      error_code="UPLOAD_ERR_NO_FILE ",
      message="Uploaded file is empty",
      status_code=400,
    )

  try:
    extracted_text = extract_document_text(
      file.filename,
      file_content
    )

    chunks = chunk_text(
      extracted_text,
      chunk_size=100,
      chunk_overlap=20
    )

    embeddings = generate_embeddings(chunks)

    document_id = str(uuid4())
    add_chunks(
      document_id=document_id,
      chunks=chunks,
      embeddings=embeddings
    )
        
    return {
      "document_id": document_id,
      "filename": file.filename,
      "content_type": file.content_type,
      "size": len(file_content),
      "chunk_count": len(chunks),
      "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
      "status": "processed"
    }

  except Exception as error:
    raise AppException(
      error_code="INTERNAL_SERVER_ERROR",
      message=f"Document processing failed: {str(error)}",
      status_code=500,
    )