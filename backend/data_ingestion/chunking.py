from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from backend.utils import log


def chunk_documents(
    docs: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Document]:
    """Split documents into chunks. Each chunk inherits the parent's metadata
    and receives a chunk_id."""
    cs = chunk_size or settings.chunk_size
    co = chunk_overlap or settings.chunk_overlap

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cs,
        chunk_overlap=co,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )

    chunks = splitter.split_documents(docs)

    # Assign a sequential id - useful for debugging and for citations.
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i

    log.info(f"Chunked {len(docs)} pages -> {len(chunks)} chunks "
             f"(size={cs}, overlap={co})")
    return chunks