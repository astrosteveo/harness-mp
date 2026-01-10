"""
Megatron MCP Server - Semantic memory for Claude Code.

Run with: python -m megatron_mcp.mcp_server
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

from .project_memory import ProjectMemory, SessionState, find_project_transcript


class MegatronMCPServer:
    """MCP Server providing semantic memory tools."""

    def __init__(self):
        self.memories: dict[str, ProjectMemory] = {}

    def get_memory(self, project_path: str) -> ProjectMemory:
        """Get or create memory for a project."""
        if project_path not in self.memories:
            self.memories[project_path] = ProjectMemory(Path(project_path))
        return self.memories[project_path]

    def handle_request(self, request: dict) -> dict:
        """Handle an MCP request."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        if method == "initialize":
            return self._initialize(req_id, params)
        elif method == "tools/list":
            return self._list_tools(req_id)
        elif method == "tools/call":
            return self._call_tool(req_id, params)
        else:
            return self._error(req_id, -32601, f"Method not found: {method}")

    def _initialize(self, req_id: Any, params: dict) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "megatron-memory",
                    "version": "1.0.0"
                }
            }
        }

    def _list_tools(self, req_id: Any) -> dict:
        tools = [
            {
                "name": "memory_search",
                "description": "Search project semantic memory for relevant past context. Use when you need to find previous discussions, decisions, or code patterns from past sessions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "What to search for (semantic search, not keyword)"
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)"
                        },
                        "n_results": {
                            "type": "integer",
                            "description": "Number of results (default 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "memory_resume",
                "description": "Get context to resume previous work. Returns last session state, active todos, plan files, and recent exchanges. Use when user says 'resume', 'continue', or 'where were we'.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)"
                        }
                    }
                }
            },
            {
                "name": "memory_remember",
                "description": "Explicitly remember something important for future sessions. Use for key decisions, user preferences, important patterns, or anything that should persist.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "What to remember"
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional tags for categorization"
                        }
                    },
                    "required": ["content"]
                }
            },
            {
                "name": "memory_sync",
                "description": "Sync memory from the current session transcript. Use to ensure latest exchanges are indexed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)"
                        }
                    }
                }
            },
            {
                "name": "memory_stats",
                "description": "Get statistics about project memory - how many chunks indexed, memory location, etc.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)"
                        }
                    }
                }
            }
        ]

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": tools}
        }

    def _call_tool(self, req_id: Any, params: dict) -> dict:
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        try:
            if tool_name == "memory_search":
                result = self._memory_search(args)
            elif tool_name == "memory_resume":
                result = self._memory_resume(args)
            elif tool_name == "memory_remember":
                result = self._memory_remember(args)
            elif tool_name == "memory_sync":
                result = self._memory_sync(args)
            elif tool_name == "memory_stats":
                result = self._memory_stats(args)
            else:
                return self._error(req_id, -32602, f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result}]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                    "isError": True
                }
            }

    def _memory_search(self, args: dict) -> str:
        query = args.get("query", "")
        project_path = args.get("project_path", str(Path.cwd()))
        n_results = args.get("n_results", 5)

        memory = self.get_memory(project_path)
        results = memory.query(query, n_results=n_results)

        if not results:
            return "No relevant memories found."

        output = [f"# Memory Search: '{query}'\n"]
        for i, result in enumerate(results, 1):
            output.append(f"## Result {i} (relevance: {result['score']:.2f})")
            output.append(result['content'])
            output.append("")

        return "\n".join(output)

    def _memory_resume(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)
        return memory.get_resume_context()

    def _memory_remember(self, args: dict) -> str:
        content = args.get("content", "")
        project_path = args.get("project_path", str(Path.cwd()))
        tags = args.get("tags", [])

        if not content:
            return "Error: No content provided to remember."

        memory = self.get_memory(project_path)

        # Create a special "remembered" chunk
        from .chunker import Chunk
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
        return f"✓ Remembered: {content[:100]}{'...' if len(content) > 100 else ''}"

    def _memory_sync(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)

        transcript = find_project_transcript(Path(project_path))
        if not transcript:
            return "No transcript found for this project."

        count = memory.index_transcript(transcript)
        return f"Synced {count} chunks from current session."

    def _memory_stats(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)
        stats = memory.get_stats()

        return f"""# Memory Stats

**Project:** {stats['project']}
**Indexed Chunks:** {stats['total_chunks']}
**Memory Path:** {stats['memory_path']}
"""

    def _error(self, req_id: Any, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message}
        }

    def run(self):
        """Run the MCP server on stdio."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line)
                response = self.handle_request(request)

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except json.JSONDecodeError:
                continue
            except KeyboardInterrupt:
                break


def main():
    server = MegatronMCPServer()
    server.run()


if __name__ == "__main__":
    main()
