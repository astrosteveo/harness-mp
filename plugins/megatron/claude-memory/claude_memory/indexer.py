"""Index conversation chunks into ChromaDB."""

from pathlib import Path
import chromadb
from chromadb.config import Settings

from .parser import parse_transcript, find_transcripts
from .chunker import chunk_by_exchange, Chunk


class MemoryIndex:
    """Manages the ChromaDB index for Claude conversation memory."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            db_path = Path.home() / ".megatron"

        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False)
        )

        # Use sentence-transformers embedding function
        # ChromaDB will handle loading the model
        self.collection = self.client.get_or_create_collection(
            name="claude_conversations",
            metadata={"hnsw:space": "cosine"},
        )

    def index_transcript(self, file_path: Path) -> int:
        """Index a single transcript file. Returns number of chunks indexed."""
        messages = list(parse_transcript(file_path))
        if not messages:
            return 0

        chunks = chunk_by_exchange(messages)
        if not chunks:
            return 0

        # Prepare batch for ChromaDB
        ids = [chunk.id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [
            {
                "session_id": chunk.session_id,
                "timestamp": chunk.timestamp,
                "source_file": str(file_path),
                **chunk.metadata,
            }
            for chunk in chunks
        ]

        # Upsert to handle re-indexing
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

        return len(chunks)

    def index_all(self, claude_dir: Path | None = None) -> dict:
        """Index all transcripts. Returns stats."""
        transcripts = find_transcripts(claude_dir)
        stats = {
            "files_processed": 0,
            "chunks_indexed": 0,
            "errors": [],
        }

        for transcript in transcripts:
            try:
                count = self.index_transcript(transcript)
                stats["files_processed"] += 1
                stats["chunks_indexed"] += count
            except Exception as e:
                stats["errors"].append(f"{transcript}: {e}")

        return stats

    def get_stats(self) -> dict:
        """Get index statistics."""
        return {
            "total_chunks": self.collection.count(),
        }

    def clear(self):
        """Clear all indexed data."""
        self.client.delete_collection("claude_conversations")
        self.collection = self.client.create_collection(
            name="claude_conversations",
            metadata={"hnsw:space": "cosine"},
        )
