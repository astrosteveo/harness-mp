# Engram MCP Plugin

Claude Code plugin for [engram](https://github.com/astrosteveo/engram) - semantic memory across sessions.

## What You Get

- **MCP Tools**: `memory_search`, `memory_resume`, `memory_remember`, `memory_sync`, `memory_stats`
- **Commands**: `/engram/remember`, `/engram/resume`, `/engram/search`, `/engram/stats`, `/engram/sync`
- **Live Indexing**: Automatically indexes conversation as you work

## Installation

```bash
git clone https://github.com/your-org/marketplace
cd marketplace/plugins/engram-mcp
./install.sh /path/to/your/project
```

Then restart Claude Code.

## Usage

```
> resume                    # Where was I?
> /engram/search "auth"     # Find past discussions
> /engram/remember "..."    # Save something important
```

## How It Works

This plugin configures Claude Code to run the engram MCP server via:
```
uvx --from git+https://github.com/astrosteveo/engram engram-mcp
```

No local installation of engram is required.

## Uninstall

```bash
./uninstall.sh /path/to/your/project
```

## More Info

See the main engram repo: https://github.com/astrosteveo/engram

## License

MIT
