from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, File, UploadFile

from app.db.mongo import documents_collection
from app.core.response import success_response
from app.schemas.document import DocumentResponse
from app.services.document_processing_service import process_document
from app.services.document_service import (
  get_document,
  get_all_documents,
  delete_document
)
from app.core.exceptions import AppException
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import add_chunks

router = APIRouter(
  prefix="/documents",
  tags=["Documents"]
)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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
    # -----------------------------------
    # 4. Create document ID
    # -----------------------------------
    document_id = str(uuid4())

    # -----------------------------------
    # 5. Create MongoDB document
    # -----------------------------------
    document = {
      "document_id": document_id,
      "filename": file.filename,
      "content_type": file.content_type,
      "size": len(file_content),
      "extracted_text": None,
      "chunk_count": 0,
      "embedding_dimensions": 0,
      "status": "uploaded",
      "error": None,
    }

    documents_collection.insert_one(document)

    # -----------------------------------
    # 6. Start background processing
    # -----------------------------------
    background_tasks.add_task(
      process_document,
      document_id=document_id,
      filename=file.filename,
      content_type=file.content_type,
      file_content=file_content,
      file_size=len(file_content),
    )

    # -----------------------------------
    # 7. Return immediately
    # -----------------------------------        
    return success_response(
      message="Document uploaded and processing started",
      data={
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_content),
        "chunk_count": 0,
        "embedding_dimensions": 0,
        "status": "processing"
      }
    )

  except Exception as error:
    raise AppException(
      error_code="INTERNAL_SERVER_ERROR",
      message=f"Document processing failed: {str(error)}",
      status_code=500,
    )

@router.get("")
async def list_documents():
  return success_response(
    message="Documents retrieved successfully",
    data = get_all_documents()
  )

@router.get("/{document_id}")
async def get_document_by_id(document_id: str):

  document = get_document(document_id)

  if not document:
    raise AppException(
      error_code="DOCUMENT_NOT_FOUND",
      message="Document not found",
      status_code=404,
    )

  return document

@router.delete("/{document_id}")
async def remove_document(document_id: str):

  document = delete_document(document_id)

  if not document:
    raise AppException(
        error_code="DOCUMENT_NOT_FOUND",
        message="Document not found for deletion: {document_id}",
        status_code=404,
      )

  return success_response(
    message="Document deleted successfully",
    data={
      "document_id": document_id
    }
  )