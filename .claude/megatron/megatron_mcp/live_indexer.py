"""Live indexer - indexes conversation chunks in real-time."""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from .project_memory import ProjectMemory, SessionState
from .chunker import Chunk


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


def extract_indexable_content(hook_input: HookInput) -> Optional[Chunk]:
    """
    Extract content worth indexing from a hook event.

    We index after significant tool uses:
    - After assistant responses (captures exchanges)
    - After file edits (captures what changed)
    - After bash commands (captures what was run)
    """
    if not hook_input.tool_name:
        return None

    # Build content from the tool interaction
    content_parts = []

    if hook_input.tool_name in ("Edit", "Write", "MultiEdit"):
        # File operations - index what was changed
        if hook_input.tool_input:
            file_path = hook_input.tool_input.get("file_path", "")
            content_parts.append(f"[Edited file: {file_path}]")
            if hook_input.tool_input.get("new_string"):
                content_parts.append(f"New content: {hook_input.tool_input['new_string'][:500]}")

    elif hook_input.tool_name == "Bash":
        # Bash commands - index the command and output
        if hook_input.tool_input:
            cmd = hook_input.tool_input.get("command", "")
            content_parts.append(f"[Command: {cmd}]")
        if hook_input.tool_output:
            output = hook_input.tool_output[:500]
            content_parts.append(f"Output: {output}")

    elif hook_input.tool_name == "TodoWrite":
        # Todo updates - index the todo state
        if hook_input.tool_input:
            todos = hook_input.tool_input.get("todos", [])
            content_parts.append("[Todo Update]")
            for todo in todos:
                status = todo.get("status", "pending")
                content = todo.get("content", "")
                content_parts.append(f"  [{status}] {content}")

    elif hook_input.tool_name == "Read":
        # File reads - light indexing of what was examined
        if hook_input.tool_input:
            file_path = hook_input.tool_input.get("file_path", "")
            content_parts.append(f"[Read file: {file_path}]")

    if not content_parts:
        return None

    content = "\n".join(content_parts)

    return Chunk(
        id=f"{hook_input.session_id}:{hook_input.tool_name}:{hash(content) % 10000}",
        content=content,
        session_id=hook_input.session_id,
        timestamp=str(Path(hook_input.transcript_path).stat().st_mtime) if hook_input.transcript_path else "",
        metadata={
            "tool": hook_input.tool_name,
            "type": "tool_use",
        }
    )


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

    from datetime import datetime
    return SessionState(
        session_id=hook_input.session_id,
        timestamp=datetime.now().isoformat(),
        cwd=str(hook_input.cwd),
        last_exchanges=[],  # Could populate from recent memory query
        active_todos=todos,
        plan_files=plan_files,
        in_progress=in_progress,
        last_error=None,  # Could extract from recent errors
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

    # Extract and index content
    chunk = extract_indexable_content(hook_input)
    if chunk:
        memory.index_chunk(chunk)

    # Capture state on significant events
    if hook_input.tool_name == "TodoWrite":
        state = capture_session_state(hook_input, memory)
        memory.save_state(state)

    # Always continue
    print('{"continue": true}')


if __name__ == "__main__":
    run_live_indexer()
