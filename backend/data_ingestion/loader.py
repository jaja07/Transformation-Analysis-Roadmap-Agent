from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from core.config import settings, FRAMEWORK_REGISTRY, FRAMEWORK_LABELS
from backend.utils import log


def load_corpus(corpus_dir: Path | None = None) -> list[Document]:
    """Load all PDFs from the corpus directory.

    Returns one Document per page, with metadata:
        source            - filename
        page              - page number
        framework         - canonical id (wade_2015, peter_2018, ...)
        framework_label   - human-readable label
    """
    corpus_dir = corpus_dir or settings.corpus_dir
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    pdfs = sorted(corpus_dir.rglob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in {corpus_dir}")

    log.info(f"Loading {len(pdfs)} PDFs from {corpus_dir}")
    docs: list[Document] = []
    for pdf in pdfs:
        framework_id = FRAMEWORK_REGISTRY.get(pdf.name, "unknown")
        framework_label = FRAMEWORK_LABELS.get(framework_id, pdf.name)

        if framework_id == "unknown":
            log.warning(f"Unmapped PDF: {pdf.name} - add it to FRAMEWORK_REGISTRY")

        # PyPDFLoader returns one Document per page
        for page in PyPDFLoader(str(pdf)).load():
            if not page.page_content.strip():
                continue  # skip empty pages (often the very last page of a PDF)
            page.metadata.update({
                "source": pdf.name,
                "framework": framework_id,
                "framework_label": framework_label,
                "page": page.metadata.get("page", 0),
            })
            docs.append(page)
        log.info(f"  {pdf.name}: tagged as '{framework_id}'")

    log.info(f"Loaded {len(docs)} non-empty pages total")
    return docs