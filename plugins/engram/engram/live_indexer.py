"""Live indexer - indexes conversation chunks in real-time."""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .project_memory import ProjectMemory, SessionState
from .chunker import Chunk
from .parser import parse_transcript


@dataclass
class HookInput:
    """Parsed hook input from Claude Code."""
    session_id: str
    cwd: Path
    hook_event: str
    tool_name: Optional[str] = None
    tool_input: Optional[dict] = None
    tool_output: Optional[str] = None
    transcript_path: Optional[Path] = None


def parse_hook_input(input_json: str) -> HookInput:
    """Parse the JSON input from a Claude Code hook."""
    data = json.loads(input_json)
    return HookInput(
        session_id=data.get("session_id", ""),
        cwd=Path(data.get("cwd", ".")),
        hook_event=data.get("hook_event_name", ""),
        tool_name=data.get("tool_name"),
        tool_input=data.get("tool_input"),
        tool_output=data.get("tool_output"),
        transcript_path=Path(data["transcript_path"]) if data.get("transcript_path") else None,
    )


def get_index_marker_path(memory_path: Path, session_id: str) -> Path:
    """Get the path to the marker file tracking indexed line count."""
    return memory_path / f".indexed_{session_id}"


def get_last_indexed_line(memory_path: Path, session_id: str) -> int:
    """Get the last indexed line number for this session."""
    marker = get_index_marker_path(memory_path, session_id)
    if marker.exists():
        try:
            return int(marker.read_text().strip())
        except (ValueError, IOError):
            pass
    return 0


def save_indexed_line(memory_path: Path, session_id: str, line_num: int) -> None:
    """Save the last indexed line number."""
    marker = get_index_marker_path(memory_path, session_id)
    marker.write_text(str(line_num))


def index_new_messages(hook_input: HookInput, memory: ProjectMemory) -> int:
    """
    Index new messages from the transcript since last run.

    Returns the number of chunks indexed.
    """
    if not hook_input.transcript_path or not hook_input.transcript_path.exists():
        return 0

    # Get current position
    last_line = get_last_indexed_line(memory.memory_path, hook_input.session_id)

    # Read and parse new messages
    messages = []
    current_line = 0

    with open(hook_input.transcript_path, "r") as f:
        for line in f:
            current_line += 1
            if current_line <= last_line:
                continue

            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Only index user and assistant messages
            msg_type = data.get("type")
            if msg_type not in ("user", "assistant"):
                continue

            # Skip meta messages
            if data.get("isMeta"):
                continue

            message_data = data.get("message", {})
            content = message_data.get("content", "")

            # Extract text content
            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)

            if not content or not content.strip():
                continue

            # Skip command-related content
            if content.startswith("<command-name>") or content.startswith("<local-command"):
                continue

            role = message_data.get("role", msg_type)
            uuid = data.get("uuid", "")
            timestamp = data.get("timestamp", "")

            messages.append({
                "role": role,
                "content": content,
                "uuid": uuid,
                "timestamp": timestamp,
            })

    # Chunk messages by exchange (user + assistant pairs)
    chunks_indexed = 0
    exchange = []

    for msg in messages:
        exchange.append(msg)

        # When we have a complete exchange, index it
        if msg["role"] == "assistant" and len(exchange) >= 1:
            content_parts = []
            for m in exchange:
                prefix = "User: " if m["role"] == "user" else "Assistant: "
                # Truncate very long messages
                msg_content = m["content"][:2000] if len(m["content"]) > 2000 else m["content"]
                content_parts.append(f"{prefix}{msg_content}")

            chunk_content = "\n\n".join(content_parts)

            # Create and index chunk
            chunk = Chunk(
                id=f"{hook_input.session_id}:exchange:{exchange[0]['uuid']}",
                content=chunk_content,
                session_id=hook_input.session_id,
                timestamp=exchange[0].get("timestamp", ""),
                metadata={
                    "type": "exchange",
                    "message_count": len(exchange),
                }
            )
            memory.index_chunk(chunk)
            chunks_indexed += 1
            exchange = []

    # Index any remaining messages (incomplete exchange)
    if exchange:
        content_parts = []
        for m in exchange:
            prefix = "User: " if m["role"] == "user" else "Assistant: "
            msg_content = m["content"][:2000] if len(m["content"]) > 2000 else m["content"]
            content_parts.append(f"{prefix}{msg_content}")

        chunk = Chunk(
            id=f"{hook_input.session_id}:partial:{exchange[0]['uuid']}",
            content="\n\n".join(content_parts),
            session_id=hook_input.session_id,
            timestamp=exchange[0].get("timestamp", ""),
            metadata={
                "type": "partial_exchange",
                "message_count": len(exchange),
            }
        )
        memory.index_chunk(chunk)
        chunks_indexed += 1

    # Save progress
    if current_line > last_line:
        save_indexed_line(memory.memory_path, hook_input.session_id, current_line)

    return chunks_indexed


def capture_session_state(hook_input: HookInput, memory: ProjectMemory) -> SessionState:
    """Capture current session state for resume capability."""
    todos = []
    in_progress = ""
    plan_files = {}

    # Try to extract todos from recent TodoWrite
    if hook_input.tool_name == "TodoWrite" and hook_input.tool_input:
        todos = hook_input.tool_input.get("todos", [])
        # Find in-progress item
        for todo in todos:
            if todo.get("status") == "in_progress":
                in_progress = todo.get("content", "")
                break

    # Look for plan files in the project
    plan_dir = hook_input.cwd / ".claude" / "plans"
    if plan_dir.exists():
        for plan_file in plan_dir.glob("*.md"):
            try:
                plan_files[str(plan_file.relative_to(hook_input.cwd))] = plan_file.read_text()[:3000]
            except:
                pass

    # Also check for CLAUDE.md or similar context files
    for context_file in ["CLAUDE.md", "claude.md", ".claude/context.md"]:
        ctx_path = hook_input.cwd / context_file
        if ctx_path.exists():
            try:
                plan_files[context_file] = ctx_path.read_text()[:2000]
            except:
                pass

    return SessionState(
        session_id=hook_input.session_id,
        timestamp=datetime.now().isoformat(),
        cwd=str(hook_input.cwd),
        last_exchanges=[],
        active_todos=todos,
        plan_files=plan_files,
        in_progress=in_progress,
        last_error=None,
    )


def run_live_indexer():
    """Main entry point for live indexing hook."""
    # Read hook input from stdin
    input_json = sys.stdin.read()
    if not input_json.strip():
        print('{"continue": true}')
        return

    try:
        hook_input = parse_hook_input(input_json)
    except (json.JSONDecodeError, KeyError):
        print('{"continue": true}')
        return

    # Get project memory
    memory = ProjectMemory(hook_input.cwd)

    # Index new conversation messages from transcript
    index_new_messages(hook_input, memory)

    # Capture state on significant events
    if hook_input.tool_name == "TodoWrite":
        state = capture_session_state(hook_input, memory)
        memory.save_state(state)

    # Always continue
    print('{"continue": true}')


if __name__ == "__main__":
    run_live_indexer()
