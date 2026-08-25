from typing import Dict, List

from app.retrieval.ingestion import ingest_documents


class DocumentStore:
    """Simple in-memory searchable document store."""

    def __init__(self):
        self.documents: List[Dict] = ingest_documents()

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Return document chunks containing the most query terms."""

        query_terms = {
            term.lower()
            for term in query.split()
            if len(term.strip()) > 2
        }

        if not query_terms:
            return []

        scored = []

        for document in self.documents:
            text = document["text"].lower()

            score = sum(
                1 for term in query_terms
                if term in text
            )

            if score > 0:
                scored.append(
                    {
                        **document,
                        "score": score,
                    }
                )

        scored.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored[:top_k]