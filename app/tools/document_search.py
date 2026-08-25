from typing import Any, Dict, List

from app.retrieval.store import DocumentStore


class DocumentSearchTool:
    """Searches the supplied ParcelPilot documents."""

    def __init__(self):
        self.store = DocumentStore()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Search the supplied documents.

        Multiple chunks can belong to the same document. For the
        support-agent interface, keep only the highest-scoring
        chunk from each unique document.
        """

        results = self.store.search(
            query=query,
            top_k=top_k,
        )

        best_by_document: Dict[str, Dict[str, Any]] = {}

        for result in results:
            document = result["document"]

            if (
                document not in best_by_document
                or result["score"] > best_by_document[document]["score"]
            ):
                best_by_document[document] = result

        formatted: List[Dict[str, Any]] = []

        for result in best_by_document.values():
            formatted.append(
                {
                    "document": result["document"],
                    "chunk_id": result["chunk_id"],
                    "score": result["score"],
                    "text": result["text"],
                }
            )

        formatted.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return {
            "query": query,
            "results": formatted,
            "result_count": len(formatted),
        }