"""
agents/retriever/nodes.py
Nodes du Retrieval Agent.
"""

from .state import RetrievalState
from .prompts import SYSTEM_PROMPT, QUERY_GENERATION_PROMPT
from ..llm_clients.nim_client import call_nim
from ..retrieval.retriever import retrieve, format_chunks


def generate_queries_node(state: RetrievalState) -> RetrievalState:
    prompt = QUERY_GENERATION_PROMPT.format(
        structured_problem=state["structured_problem"]
    )
    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.1,
        max_tokens=256,
    )
    print(f"[DEBUG] Réponse brute LLM:\n{response}\n")  # ← ajoute ça
    queries = [q.strip() for q in response.strip().splitlines() if q.strip()]
    queries = queries[:3]
    while len(queries) < 3:
        queries.append(state["structured_problem"][:200])
    return {**state, "_queries": queries}


def retrieve_node(state: RetrievalState) -> RetrievalState:
    """
    Node 2 : interroge ChromaDB avec les 3 queries et structure les contextes.
    """
    queries = state.get("_queries", [])

    # Retrieval ciblé par dimension
    why_chunks  = retrieve(queries[0], n_results=4)
    what_chunks = retrieve(queries[1], n_results=4)
    how_chunks  = retrieve(queries[2], n_results=4)

    # Formatage pour injection dans les prompts des agents suivants
    why_context  = format_chunks(why_chunks,  max_chars=2000)
    what_context = format_chunks(what_chunks, max_chars=2000)
    how_context  = format_chunks(how_chunks,  max_chars=2000)

    # Contexte global = union dédupliquée des meilleurs chunks
    all_texts = {c["text"] for c in why_chunks + what_chunks + how_chunks}
    global_context = "\n\n".join(list(all_texts)[:8])  # max 8 chunks uniques

    return {
        **state,
        "why_context": why_context,
        "what_context": what_context,
        "how_context": how_context,
        "global_context": global_context,
    }