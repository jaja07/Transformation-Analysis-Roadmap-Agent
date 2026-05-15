# Import des modules
from functools import lru_cache
from typing import Iterable, Union

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from core.config import settings
from utils import log
from vector_store import load_index

# Abstraction layer above the FAISS index to simplify queries and standardize results.
class CorpusRetriever:
    def __init__(
        self,
        store: FAISS,
        default_k: int | None = None,
        default_fetch_k: int | None = None,
        default_lambda: float | None = None,
    ):
        self.store = store
        self.default_k = default_k or settings.retrieval_top_k
        self.default_fetch_k = default_fetch_k or settings.retrieval_fetch_k
        self.default_lambda = default_lambda or settings.retrieval_lambda

    # ------------------------------------------------------------------
    # Search for the top-k relevant chunks for the query
    # ------------------------------------------------------------------
    def search(
        self,
        query: str,                              # request to match
        k: int | None = None,                    # number of chunks to return
        frameworks: Iterable[str] | None = None, # if specified, filter only on these framework_ids
        use_mmr: bool = True,
    ) -> list[Document]:
        """Return top-k passages, optionally restricted to specific frameworks."""
        k = k or self.default_k 
        filter_fn = None
        
        if frameworks:
            target = set(frameworks)
            filter_fn = lambda meta: meta.get("framework") in target  # noqa: E731

        if use_mmr:
            # On fetch davantage de candidats puis on filtre+diversifie
            results = self.store.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=self.default_fetch_k,
                lambda_mult=self.default_lambda, 
                filter=filter_fn,
            )
        else:
            results = self.store.similarity_search(
                query=query,
                k=k,
                filter=filter_fn,
            )

        log.debug(
            f"Retrieval: query={repr(query)[:60]} | k={k} | "
            f"frameworks={list(frameworks) if frameworks else 'all'} | "
            f"mmr={use_mmr} | got={len(results)}"
        )
        return results 

    # ------------------------------------------------------------------
    # Several sub-queries and deduplicate by chunk_id
    # ------------------------------------------------------------------
    def multi_query_retrieve(
        self,
        queries: Iterable[str],
        framework: str | None = None,
        per_query_k: int = 2,
    ) -> list[Document]:
        """Run several sub-queries and deduplicate by chunk_id."""
        seen: set = set()
        merged: list[Document] = []
        
        # Format the single framework into a list for the search method
        fw_list = [framework] if framework else None

        for q in queries:
            for d in self.search(query=q, frameworks=fw_list, k=per_query_k):
                # Utiliser id(d) comme fallback si chunk_id est manquant pour éviter de supprimer des docs valides
                cid = d.metadata.get("chunk_id", id(d)) 
                if cid in seen:
                    continue
                seen.add(cid)
                merged.append(d)
        return merged

    # ------------------------------------------------------------------
    # Expert Context: Combine Multi-Query and Multi-Framework
    # ------------------------------------------------------------------
    def retrieve_expert_context(
        self,
        queries: str | Iterable[str],
        frameworks: list[str] | None = None,
        per_query_k: int = 2,
        as_dict: bool = False
    ) -> Union[list[Document], dict[str, list[Document]]]:
        """Combines query expansion and framework filtering."""
        
        # Input normalization: a single string is transformed into a list
        query_list = [queries] if isinstance(queries, str) else list(queries)
        
        # If no framework is specified, a global deduplicated search is performed
        if not frameworks:
            return self.multi_query_retrieve(query_list, framework=None, per_query_k=per_query_k)

        # Multi-framework search
        results_by_framework = {}
        for fw in frameworks:
            # We use multi_query_retrieve for each framework to be exhaustive
            results_by_framework[fw] = self.multi_query_retrieve(
                query_list, 
                framework=fw, 
                per_query_k=per_query_k
            )

        # Return as needed by the agent
        if as_dict:
            return results_by_framework
        
        # Otherwise, we flatten and deduplicate globally
        all_docs = [doc for docs in results_by_framework.values() for doc in docs]
        return self._deduplicate(all_docs)

    def _deduplicate(self, documents: list[Document]) -> list[Document]:
        """Private utility to clean duplicates by chunk_id."""
        seen = set()
        unique_docs = []
        for doc in documents:
            cid = doc.metadata.get("chunk_id", id(doc))
            if cid not in seen:
                seen.add(cid)
                unique_docs.append(doc)
        return unique_docs


# ----------------------------------------------------------------------------
# Helper de formatage pour injection dans les prompts
# ----------------------------------------------------------------------------
def format_chunks_for_prompt(
    chunks: list[Document],
    max_chars_per_chunk: int = 800,
) -> str:
    """Format a list of chunks for readable injection into an LLM prompt."""
    blocks = []
    for chunk in chunks:
        label = chunk.metadata.get("framework_label", chunk.metadata.get("source", "?"))
        page = chunk.metadata.get("page", "?")
        content = chunk.page_content.strip()
        if len(content) > max_chars_per_chunk:
            content = content[:max_chars_per_chunk] + " […]"
        blocks.append(f"[Source: {label} | page {page}]\n{content}")
    return "\n\n---\n\n".join(blocks)


# ----------------------------------------------------------------------------
# Single instance of the retriever for the entire app
# ----------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_retriever() -> CorpusRetriever:
    store = load_index()
    return CorpusRetriever(store=store)


def retriever_node(state) -> dict:
    """Retrieve corpus context for the current business case."""
    print("--- [RETRIEVER] Recherche du contexte documentaire ---")

    business_case = state["business_case"]
    retriever = get_retriever()
    
    # On commence avec les requêtes de base
    queries = [business_case.company_name, business_case.context_text]
    
    # SI l'utilisateur a uploadé un document, on utilise le début du document 
    # (les 1000 premiers caractères) comme requête supplémentaire pour trouver les bons frameworks
    if business_case.document_content:
        doc_snippet = business_case.document_content[:1000]
        queries.append(f"Analyse ce contexte métier : {doc_snippet}")

    documents = retriever.retrieve_expert_context(
        queries=queries,
        per_query_k=3,
    )

    if isinstance(documents, dict):
        flattened_documents = [doc for docs in documents.values() for doc in docs]
    else:
        flattened_documents = documents

    return {"retrieved_context": format_chunks_for_prompt(flattened_documents)}