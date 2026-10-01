from app.worker.celery_app import celery_app
from app.services.document_processing_service import process_document

@celery_app.task
def process_document_task(
  document_id: str,
  filename: str,
  content_type: str | None,
  file_content: bytes,
  file_size: int,
):
  process_document(
    document_id=document_id,
    filename=filename,
    content_type=content_type,
    file_content=file_content,
    file_size=file_size,
  )