from io import BytesIO # BytesIO allows us to treat bytes in memory like a file. We don't necessarily need to save the PDF to disk first.

from pypdf import PdfReader

ALLOWED_EXTENSIONS = {".pdf", ".txt"}

def extract_text_from_txt(file_content: bytes) -> str:
  return file_content.decode("utf-8")

def extract_text_from_pdf(file_content: bytes) -> str:
  pdf_file = BytesIO(file_content)

  reader = PdfReader(pdf_file)

  extracted_text = []

  for page in reader.pages:
    text = page.extract_text()

    if text:
      extracted_text.append(text)

  return "\n".join(extracted_text)

def extract_document_text(filename: str, file_content: bytes) -> str:
  extension = filename.lower().rsplit(".", 1)[-1]

  if extension == "txt":
    return extract_text_from_txt(file_content)

  if extension == "pdf":
    return extract_text_from_pdf(file_content)

  raise ValueError("Unsupported file type")