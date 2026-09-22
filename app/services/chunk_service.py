from typing import List

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:

  if not text:
    return []

  if chunk_overlap >= chunk_size:
    raise ValueError(
      "chunk_overlap must be smaller than chunk_size"
    )

  chunks = []

  start = 0
  text_length = len(text)

  while start < text_length:
    end = start + chunk_size

    chunk = text[start:end].strip()

    if chunk:
      chunks.append(chunk)

    start = end - chunk_overlap

  return chunks