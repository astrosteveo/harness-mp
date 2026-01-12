# Harness

Feature development workflows and plugin creation skills for Claude Code.

Harness bootstraps your project with skills and agents that live in `.claude/`, checked into version control, and evolve with your project.

## Installation

### Via Claude Command (recommended)

If harness is installed as a plugin:

```
/harness:init            # First install - skip existing
/harness:init --update   # Smart update - preserve customizations
/harness:init --force    # Overwrite everything
```

### Via Script

Run the init script directly:

```bash
/path/to/harness/scripts/init.sh                    # First install
/path/to/harness/scripts/init.sh --update           # Smart update
/path/to/harness/scripts/init.sh --force            # Overwrite all
/path/to/harness/scripts/init.sh /path/to/project   # Specify target
```

### How `--update` Works

- Tracks installed file checksums in `.claude/.harness-manifest`
- Files you haven't modified -> updated to latest
- Files you've customized -> preserved (listed in output)

## What Gets Installed

Skills and agents are copied to your project's `.claude/` directory:

```
your-project/
└── .claude/
    ├── skills/           # 21 development skills
    ├── agents/           # 6 specialized agents
    └── .harness-manifest # Tracks installed versions
```

## Feature Development Workflow

Guided workflow for building features from discovery to completion:

| Skill | Purpose |
|-------|---------|
| `/harness:orchestrator` | Full guided workflow from start to finish |
| `/harness:feature-discovery` | Initialize a new feature, create artifacts directory |
| `/harness:explore-codebase` | Deep exploration to understand patterns and architecture |
| `/harness:gather-requirements` | Systematically identify and resolve ambiguities |
| `/harness:design-architecture` | Design multiple approaches with trade-offs |
| `/harness:implement-feature` | Build following the designed architecture |
| `/harness:review-code` | Review for bugs, quality, conventions |
| `/harness:verify-testing` | Generate testing checklist, guide verification |
| `/harness:summarize-feature` | Document what was built, decisions, lessons |
| `/harness:red-green-refactor` | TDD workflow for testable functionality |

## Plugin Development

Create project-specific skills, agents, hooks, and commands:

| Skill | Purpose |
|-------|---------|
| `/harness:skill-development` | Create new skills with proper structure |
| `/harness:agent-development` | Create autonomous agents with system prompts |
| `/harness:command-development` | Create slash commands with arguments |
| `/harness:hook-development` | Create event hooks (PreToolUse, PostToolUse, etc.) |
| `/harness:plugin-structure` | Scaffold complete plugin directory layout |
| `/harness:mcp-integration` | Add MCP servers to plugins |
| `/harness:lsp-integration` | Add language server support |
| `/harness:plugin-settings` | Add configurable settings to plugins |

## The Workflow

```
/harness:orchestrator
    │
    ├── feature-discovery     # What are we building?
    ├── explore-codebase      # How does existing code work?
    ├── gather-requirements   # What exactly do we need?
    ├── design-architecture   # How should we build it?
    ├── implement-feature     # Build it
    ├── review-code           # Check quality
    ├── verify-testing        # Manual testing
    └── summarize-feature     # Document it
```

Each step creates artifacts in `.artifacts/<feature-name>/` for tracking progress.

## Why Template-Based?

Unlike traditional plugins, harness bootstraps files into your project because:

1. **Version Control**: Skills evolve with your project through git
2. **Team Sharing**: Everyone gets the same workflows when they clone
3. **Customization**: Modify skills for your specific project needs
4. **Code Review**: Changes to workflows go through your normal review process

Use `--update` to pull in upstream improvements while preserving your customizations.

## License

MIT
