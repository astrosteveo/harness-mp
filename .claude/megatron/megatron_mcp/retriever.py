"""Retrieve relevant context from the memory index."""

from pathlib import Path
from dataclasses import dataclass

from .indexer import MemoryIndex


@dataclass
class RetrievalResult:
    """A single retrieval result."""
    content: str
    score: float
    session_id: str
    timestamp: str
    metadata: dict


class MemoryRetriever:
    """Retrieve relevant conversation context."""

    def __init__(self, db_path: Path | None = None):
        self.index = MemoryIndex(db_path)

    def query(
        self,
        query: str,
        n_results: int = 5,
        session_filter: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Query for relevant context.

        Args:
            query: What you're looking for / working on
            n_results: Number of results to return
            session_filter: Optionally filter to a specific session

        Returns:
            List of relevant conversation chunks, ranked by relevance
        """
        where = None
        if session_filter:
            where = {"session_id": session_filter}

        results = self.index.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        # Unpack results
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieval_results = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            # Convert distance to similarity score (cosine distance -> similarity)
            score = 1 - dist

            retrieval_results.append(RetrievalResult(
                content=doc,
                score=score,
                session_id=meta.get("session_id", ""),
                timestamp=meta.get("timestamp", ""),
                metadata=meta,
            ))

        return retrieval_results

    def get_context_prompt(
        self,
        query: str,
        n_results: int = 3,
        max_chars: int = 4000,
    ) -> str:
        """
        Get a formatted context prompt to inject into a new session.

        This is the main interface for carrying context across sessions.
        """
        results = self.query(query, n_results=n_results)

        if not results:
            return ""

        context_parts = [
            "# Relevant Context from Previous Sessions\n",
            "The following excerpts from previous conversations may be relevant:\n",
        ]

        total_chars = sum(len(p) for p in context_parts)

        for i, result in enumerate(results, 1):
            excerpt = f"\n## Excerpt {i} (relevance: {result.score:.2f})\n"
            excerpt += f"*Session: {result.session_id[:8]}... | {result.timestamp}*\n\n"
            excerpt += result.content
            excerpt += "\n"

            if total_chars + len(excerpt) > max_chars:
                break

            context_parts.append(excerpt)
            total_chars += len(excerpt)

        context_parts.append("\n---\n")

        return "".join(context_parts)
