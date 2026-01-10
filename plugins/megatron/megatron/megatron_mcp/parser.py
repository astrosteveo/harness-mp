"""Parse Claude Code JSONL transcript files."""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Message:
    """A single message from a Claude Code conversation."""
    uuid: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    session_id: str
    parent_uuid: str | None = None
    is_thinking: bool = False
    is_tool_use: bool = False
    tool_name: str | None = None


def parse_transcript(file_path: Path) -> Iterator[Message]:
    """Parse a JSONL transcript file and yield Message objects."""
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Skip non-message entries (file snapshots, etc.)
            msg_type = data.get("type")
            if msg_type not in ("user", "assistant"):
                continue

            # Skip meta messages
            if data.get("isMeta"):
                continue

            message_data = data.get("message", {})
            content = message_data.get("content", "")

            # Handle content that's an array (tool use, thinking, etc.)
            if isinstance(content, list):
                text_parts = []
                is_thinking = False
                is_tool_use = False
                tool_name = None

                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif block.get("type") == "thinking":
                            is_thinking = True
                            # Optionally include thinking content
                            # text_parts.append(f"[Thinking: {block.get('thinking', '')}]")
                        elif block.get("type") == "tool_use":
                            is_tool_use = True
                            tool_name = block.get("name")
                            text_parts.append(f"[Tool: {tool_name}]")

                content = "\n".join(text_parts)

                if not content.strip():
                    continue

                yield Message(
                    uuid=data.get("uuid", ""),
                    role=message_data.get("role", msg_type),
                    content=content,
                    timestamp=data.get("timestamp", ""),
                    session_id=data.get("sessionId", ""),
                    parent_uuid=data.get("parentUuid"),
                    is_thinking=is_thinking,
                    is_tool_use=is_tool_use,
                    tool_name=tool_name,
                )
            elif isinstance(content, str) and content.strip():
                # Skip command-related content
                if content.startswith("<command-name>") or content.startswith("<local-command"):
                    continue

                yield Message(
                    uuid=data.get("uuid", ""),
                    role=message_data.get("role", msg_type),
                    content=content,
                    timestamp=data.get("timestamp", ""),
                    session_id=data.get("sessionId", ""),
                    parent_uuid=data.get("parentUuid"),
                )


def find_transcripts(claude_dir: Path | None = None) -> list[Path]:
    """Find all Claude Code transcript files."""
    if claude_dir is None:
        claude_dir = Path.home() / ".claude" / "projects"

    if not claude_dir.exists():
        return []

    return list(claude_dir.rglob("*.jsonl"))
