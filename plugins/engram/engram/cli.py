"""CLI for Engram - Semantic memory for Claude Code."""

import json
import click
from pathlib import Path

from .project_memory import ProjectMemory, find_project_transcript


@click.group()
def main():
    """Engram - Semantic memory for Claude Code sessions."""
    pass


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path),
              help="Project directory (defaults to current)")
@click.option("--mcp-mode", type=click.Choice(["uvx", "local"]),
              help="How Claude invokes the MCP server (prompts if not specified)")
@click.option("--no-mcp", is_flag=True, help="Skip MCP configuration")
def init(project: Path | None, mcp_mode: str | None, no_mcp: bool):
    """Initialize engram for a project.

    Sets up:
    - .engram/ directory for memory storage
    - .mcp.json config for Claude Code integration
    - Indexes any existing transcripts

    MCP modes:
    - uvx: Uses 'uvx engram-mcp' (no install required)
    - local: Uses 'engram-mcp' (requires engram installed)
    """
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    click.echo(f"Initializing engram for: {project}")
    click.echo(f"  Memory: {memory.memory_path}")

    # Set up MCP config
    if not no_mcp:
        # Prompt for mode if not specified
        if mcp_mode is None:
            mcp_mode = click.prompt(
                "How should Claude invoke the MCP server?",
                type=click.Choice(["uvx", "local"]),
                default="uvx"
            )

        # Build server config based on mode
        if mcp_mode == "uvx":
            server_config = {"command": "uvx", "args": ["--from", "git+https://github.com/astrosteveo/engram", "engram-mcp"]}
        else:
            server_config = {"command": "engram-mcp"}

        mcp_file = project / ".mcp.json"
        if mcp_file.exists():
            try:
                config = json.loads(mcp_file.read_text())
                config.setdefault("mcpServers", {})["engram"] = server_config
                mcp_file.write_text(json.dumps(config, indent=2) + "\n")
                click.echo(f"  MCP: Updated .mcp.json (mode: {mcp_mode})")
            except json.JSONDecodeError:
                click.echo("  MCP: Could not parse .mcp.json, skipping")
        else:
            config = {"mcpServers": {"engram": server_config}}
            mcp_file.write_text(json.dumps(config, indent=2) + "\n")
            click.echo(f"  MCP: Created .mcp.json (mode: {mcp_mode})")

    # Add .engram to .gitignore if it exists
    gitignore = project / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        if ".engram/" not in content:
            with open(gitignore, "a") as f:
                f.write("\n# Engram memory\n.engram/\n")
            click.echo("  Git: Added .engram/ to .gitignore")

    # Try to find and index existing transcripts
    transcript = find_project_transcript(project)
    if transcript:
        click.echo(f"  Transcript: {transcript.name}")
        count = memory.index_transcript(transcript)
        click.echo(f"  Indexed: {count} chunks")
    else:
        click.echo("  Transcript: None found (will index on first sync)")

    click.echo("\nDone! Restart Claude Code to enable memory tools.")


@main.command()
@click.argument("query")
@click.option("-n", "--num-results", default=5, help="Number of results")
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def search(query: str, num_results: int, project: Path | None):
    """Search project memory."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    results = memory.query(query, n_results=num_results)

    if not results:
        click.echo("No results found.")
        return

    for i, result in enumerate(results, 1):
        click.echo(f"\n{'='*60}")
        click.echo(f"Result {i} | Score: {result['score']:.3f}")
        click.echo(f"{'='*60}")
        click.echo(result['content'])


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def resume(project: Path | None):
    """Get resume context for continuing work."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    context = memory.get_resume_context()
    click.echo(context)


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def stats(project: Path | None):
    """Show memory statistics."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    stats = memory.get_stats()
    click.echo(f"Project: {stats['project']}")
    click.echo(f"Indexed chunks: {stats['total_chunks']}")
    click.echo(f"Memory path: {stats['memory_path']}")


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def sync(project: Path | None):
    """Sync memory from latest transcript."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    transcript = find_project_transcript(project)
    if not transcript:
        click.echo("No transcript found for this project.")
        return

    count = memory.index_transcript(transcript)
    click.echo(f"Synced {count} chunks from {transcript.name}")


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def cleanup(project: Path | None):
    """Remove duplicate chunks from old ID format.

    This cleans up duplicates created when content was indexed by both
    the live indexer and batch sync with different ID formats.
    """
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    stats = memory.cleanup_duplicates()
    click.echo(f"Cleanup complete:")
    click.echo(f"  Scanned: {stats['scanned']} chunks")
    click.echo(f"  Removed: {stats['removed']} duplicates")
    click.echo(f"  Kept: {stats['kept']} chunks")


@main.command()
@click.argument("content")
@click.option("--tags", "-t", multiple=True, help="Tags for categorization")
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def remember(content: str, tags: tuple, project: Path | None):
    """Explicitly save something to memory."""
    from datetime import datetime
    from .chunker import Chunk

    project = project or Path.cwd()
    memory = ProjectMemory(project)

    chunk = Chunk(
        id=f"remembered:{hash(content) % 100000}:{datetime.now().isoformat()}",
        content=f"[REMEMBERED] {content}",
        session_id="manual",
        timestamp=datetime.now().isoformat(),
        metadata={
            "type": "remembered",
            "tags": ",".join(tags) if tags else "",
        }
    )

    memory.index_chunk(chunk)
    click.echo(f"Remembered: {content[:100]}{'...' if len(content) > 100 else ''}")


if __name__ == "__main__":
    main()
