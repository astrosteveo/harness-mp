# Harness

Feature development workflows and plugin creation skills for Claude Code.

## Installation

```bash
claude plugin add harness@astrosteveo-marketplace
```

## Quick Start

```bash
/harness:feature "add user authentication"
```

That's it. The command orchestrates the entire workflow, pausing only when your input is needed.

## Feature Development

### The `/harness:feature` Command

One command drives the entire development lifecycle:

```bash
/harness:feature <description>        # Start new feature
/harness:feature                      # Resume from artifacts
/harness:feature --phase design       # Jump to specific phase
/harness:feature --tdd                # Use test-driven development
/harness:feature --skip review        # Skip a phase
```

### Workflow Phases

| Phase | What Happens |
|-------|--------------|
| **Discovery** | Initialize tracking, understand the request |
| **Explore** | Deep codebase analysis via parallel `code-explorer` agents |
| **Requirements** | Clarify ambiguities one question at a time |
| **Design** | Multiple approaches via parallel `code-architect` agents |
| **Implement** | Build following approved design (or TDD if `--tdd`) |
| **Review** | Quality review via parallel `code-reviewer` agents |
| **Testing** | Manual testing verification |
| **Summary** | Document decisions and lessons learned |

### Pause Points

The workflow runs autonomously, stopping only when your input is needed:

- **Requirements** - answering clarifying questions
- **Design** - selecting an architecture approach
- **Implementation** - approving the plan before coding
- **Testing** - confirming tests pass

### Artifacts

Progress is tracked in `.artifacts/<feature-slug>/`:

```
.artifacts/user-auth/
├── progress.md      # Current phase, session log
├── requirements.md  # Clarifications and requirements
├── design.md        # Chosen approach and rationale
├── plan.md          # Implementation steps
└── summary.md       # Final documentation
```

### Memory Integration

If you have `engram-mcp` installed, `/harness:feature` automatically:

- **Searches** past sessions for relevant context at start
- **Remembers** key decisions and lessons at completion
- **Syncs** the session for future recall

## Configuration

Create `.claude/harness.yaml` for project-specific settings:

```yaml
phases:
  skip: []  # discovery, explore, requirements, design, implement, review, testing, summary

tdd:
  mode: recommend  # recommend | always | never

agents:
  parallel-count: 3
  models:
    explorer: sonnet
    architect: opus
    reviewer: opus

artifacts:
  directory: .artifacts
  git:
    auto-commit: true
    commit-style: conventional
```

User-level config at `~/.claude/harness.yaml` applies to all projects.

## Agents

Specialized agents launched by `/harness:feature`:

| Agent | Phase | Purpose |
|-------|-------|---------|
| `code-explorer` | Explore | Traces execution paths, maps architecture |
| `code-architect` | Design | Proposes implementation approaches |
| `code-reviewer` | Review | Checks quality, bugs, conventions |

Additional agents for plugin development:

| Agent | Purpose |
|-------|---------|
| `agent-creator` | Creates new agents |
| `plugin-validator` | Validates plugin structure |
| `skill-reviewer` | Reviews skill quality |

## Plugin Development Skills

Create Claude Code plugins with guided workflows:

| Skill | Purpose |
|-------|---------|
| `harness:plugin-structure` | Scaffold plugin directory layout |
| `harness:skill-development` | Create skills with proper structure |
| `harness:agent-development` | Create autonomous agents |
| `harness:command-development` | Create slash commands |
| `harness:hook-development` | Create event hooks |
| `harness:mcp-integration` | Add MCP servers |
| `harness:lsp-integration` | Add language server support |
| `harness:plugin-settings` | Add configurable settings |

## License

MIT
