"""CLI for Claude Memory - The Megatron."""

import click
from pathlib import Path

from .indexer import MemoryIndex
from .retriever import MemoryRetriever
from .parser import find_transcripts
from .project_memory import ProjectMemory, get_project_memory, find_project_transcript


@click.group()
def main():
    """Claude Memory - Semantic context for Claude Code sessions."""
    pass


# =============================================================================
# PROJECT-LOCAL COMMANDS (Megatron)
# =============================================================================

@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path),
              help="Project directory (defaults to current)")
def init(project: Path | None):
    """Initialize project-local memory."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    click.echo(f"Initialized memory for: {project}")
    click.echo(f"Memory stored in: {memory.memory_path}")

    # Try to find and index existing transcripts
    transcript = find_project_transcript(project)
    if transcript:
        click.echo(f"Found transcript: {transcript}")
        count = memory.index_transcript(transcript)
        click.echo(f"Indexed {count} chunks from current session")


@main.command("project-search")
@click.argument("query")
@click.option("-n", "--num-results", default=5, help="Number of results")
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def project_search(query: str, num_results: int, project: Path | None):
    """Search project-local memory."""
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


@main.command("project-stats")
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def project_stats(project: Path | None):
    """Show project memory statistics."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    stats = memory.get_stats()
    click.echo(f"Project: {stats['project']}")
    click.echo(f"Indexed chunks: {stats['total_chunks']}")
    click.echo(f"Memory path: {stats['memory_path']}")


@main.command()
@click.option("--project", "-p", type=click.Path(exists=True, path_type=Path))
def sync(project: Path | None):
    """Sync project memory from latest transcript."""
    project = project or Path.cwd()
    memory = ProjectMemory(project)

    transcript = find_project_transcript(project)
    if not transcript:
        click.echo("No transcript found for this project.")
        return

    click.echo(f"Syncing from: {transcript}")
    count = memory.index_transcript(transcript)
    click.echo(f"Indexed {count} chunks")


# =============================================================================
# GLOBAL COMMANDS (Original)
# =============================================================================

@main.command()
@click.option("--claude-dir", type=click.Path(exists=True, path_type=Path), help="Claude projects directory")
def index(claude_dir: Path | None):
    """Index all Claude Code transcripts (global)."""
    click.echo("Indexing Claude Code transcripts...")

    memory = MemoryIndex()
    stats = memory.index_all(claude_dir)

    click.echo(f"Processed {stats['files_processed']} files")
    click.echo(f"Indexed {stats['chunks_indexed']} conversation chunks")

    if stats["errors"]:
        click.echo(f"Errors: {len(stats['errors'])}")
        for error in stats["errors"][:5]:
            click.echo(f"  - {error}")


@main.command()
@click.argument("query")
@click.option("-n", "--num-results", default=5, help="Number of results to return")
@click.option("--format", "output_format", type=click.Choice(["full", "brief", "prompt"]), default="full")
def search(query: str, num_results: int, output_format: str):
    """Search for relevant context from past conversations (global)."""
    retriever = MemoryRetriever()

    if output_format == "prompt":
        prompt = retriever.get_context_prompt(query, n_results=num_results)
        if prompt:
            click.echo(prompt)
        else:
            click.echo("No relevant context found.")
        return

    results = retriever.query(query, n_results=num_results)

    if not results:
        click.echo("No relevant context found.")
        return

    for i, result in enumerate(results, 1):
        click.echo(f"\n{'='*60}")
        click.echo(f"Result {i} | Score: {result.score:.3f}")
        click.echo(f"Session: {result.session_id[:12]}...")
        click.echo(f"Time: {result.timestamp}")
        click.echo(f"{'='*60}")

        if output_format == "brief":
            content = result.content[:300] + "..." if len(result.content) > 300 else result.content
            click.echo(content)
        else:
            click.echo(result.content)


@main.command()
def stats():
    """Show global index statistics."""
    memory = MemoryIndex()
    index_stats = memory.get_stats()

    transcripts = find_transcripts()

    click.echo(f"Transcript files found: {len(transcripts)}")
    click.echo(f"Indexed chunks: {index_stats['total_chunks']}")


@main.command()
@click.confirmation_option(prompt="Are you sure you want to clear the global index?")
def clear():
    """Clear all globally indexed data."""
    memory = MemoryIndex()
    memory.clear()
    click.echo("Global index cleared.")


@main.command()
def list_sessions():
    """List all indexed sessions (global)."""
    memory = MemoryIndex()

    results = memory.collection.get(include=["metadatas"])
    metadatas = results.get("metadatas", [])

    sessions = {}
    for meta in metadatas:
        session_id = meta.get("session_id", "unknown")
        if session_id not in sessions:
            sessions[session_id] = {
                "count": 0,
                "first_timestamp": meta.get("timestamp", ""),
            }
        sessions[session_id]["count"] += 1

    if not sessions:
        click.echo("No sessions indexed yet. Run 'claude-memory index' first.")
        return

    click.echo(f"Found {len(sessions)} sessions:\n")
    for session_id, info in sorted(sessions.items(), key=lambda x: x[1]["first_timestamp"], reverse=True):
        click.echo(f"  {session_id[:12]}... | {info['count']} chunks | {info['first_timestamp'][:10]}")


if __name__ == "__main__":
    main()
