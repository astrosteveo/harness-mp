"""Project-local memory - the Megatron core."""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import chromadb
from chromadb.config import Settings

from .parser import parse_transcript
from .chunker import chunk_by_exchange, Chunk


@dataclass
class SessionState:
    """Snapshot of session state for seamless resume."""
    session_id: str
    timestamp: str
    cwd: str
    last_exchanges: list[dict]  # Recent conversation chunks
    active_todos: list[dict]    # Current todo items
    plan_files: dict[str, str]  # path -> content of active plan files
    in_progress: str            # What was being worked on
    last_error: Optional[str]   # Any recent error/blocker


class ProjectMemory:
    """
    Project-local semantic memory.

    Each project gets its own:
    - Vector index (ChromaDB)
    - State snapshots
    - Isolated context
    """

    MEMORY_DIR = ".megatron"

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.memory_path = self.project_path / self.MEMORY_DIR
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Project-local ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.memory_path / "index"),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="project_memory",
            metadata={"hnsw:space": "cosine"},
        )

    def index_chunk(self, chunk: Chunk) -> None:
        """Index a single chunk immediately (for live indexing)."""
        self.collection.upsert(
            ids=[chunk.id],
            documents=[chunk.content],
            metadatas=[{
                "session_id": chunk.session_id,
                "timestamp": chunk.timestamp,
                **chunk.metadata,
            }],
        )

    def index_transcript(self, transcript_path: Path) -> int:
        """Index a full transcript file."""
        messages = list(parse_transcript(transcript_path))
        if not messages:
            return 0

        chunks = chunk_by_exchange(messages)
        for chunk in chunks:
            self.index_chunk(chunk)

        return len(chunks)

    def query(
        self,
        query: str,
        n_results: int = 5,
    ) -> list[dict]:
        """Query project memory."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {
                "content": doc,
                "score": 1 - dist,
                "metadata": meta,
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

    def save_state(self, state: SessionState) -> None:
        """Save session state for resume capability."""
        state_file = self.memory_path / "state.json"
        with open(state_file, "w") as f:
            json.dump(asdict(state), f, indent=2)

    def load_state(self) -> Optional[SessionState]:
        """Load the last session state."""
        state_file = self.memory_path / "state.json"
        if not state_file.exists():
            return None

        with open(state_file, "r") as f:
            data = json.load(f)
            return SessionState(**data)

    def get_resume_context(self, n_recent: int = 3) -> str:
        """
        Get context for resuming work.

        Combines:
        - Last session state
        - Recent exchanges from memory
        - Any active plans/todos
        """
        parts = ["# Resume Context\n"]

        # Load last state
        state = self.load_state()
        if state:
            parts.append(f"## Last Session")
            parts.append(f"*{state.timestamp}*\n")

            if state.in_progress:
                parts.append(f"**Working on:** {state.in_progress}\n")

            if state.active_todos:
                parts.append("**Active Todos:**")
                for todo in state.active_todos:
                    status = todo.get("status", "pending")
                    icon = "🔄" if status == "in_progress" else "⬜" if status == "pending" else "✅"
                    parts.append(f"  {icon} {todo.get('content', '')}")
                parts.append("")

            if state.last_error:
                parts.append(f"**Last Blocker:** {state.last_error}\n")

            if state.plan_files:
                parts.append("**Active Plans:**")
                for path, content in state.plan_files.items():
                    parts.append(f"\n### {path}")
                    # Truncate if too long
                    if len(content) > 1500:
                        content = content[:1500] + "\n...(truncated)"
                    parts.append(f"```\n{content}\n```")
                parts.append("")

        # Query for recent context
        recent = self.query("recent work progress tasks", n_results=n_recent)
        if recent:
            parts.append("## Recent Context\n")
            for i, result in enumerate(recent, 1):
                parts.append(f"### Exchange {i} (relevance: {result['score']:.2f})")
                content = result['content']
                if len(content) > 800:
                    content = content[:800] + "\n...(truncated)"
                parts.append(content)
                parts.append("")

        parts.append("---")
        return "\n".join(parts)

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "project": str(self.project_path),
            "total_chunks": self.collection.count(),
            "memory_path": str(self.memory_path),
        }


def get_project_memory(cwd: Optional[Path] = None) -> ProjectMemory:
    """Get or create project memory for the current/specified directory."""
    if cwd is None:
        cwd = Path.cwd()
    return ProjectMemory(cwd)


def find_project_transcript(project_path: Path) -> Optional[Path]:
    """Find the most recent transcript for a project."""
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return None

    project_path = Path(project_path).resolve()

    # Try exact match first, then parent directories
    paths_to_try = [project_path]

    # Add parent paths up to home
    current = project_path
    while current != current.parent and current != Path.home():
        current = current.parent
        paths_to_try.append(current)

    for path in paths_to_try:
        # Encode path the way Claude does (replace / with -)
        encoded = str(path).replace("/", "-")
        project_transcript_dir = claude_projects / encoded

        if project_transcript_dir.exists():
            transcripts = list(project_transcript_dir.glob("*.jsonl"))
            if transcripts:
                return max(transcripts, key=lambda p: p.stat().st_mtime)

    return None
