---
name: lsp-integration
description: This skill should be used when the user asks to "add LSP server", "configure language server", "add code intelligence", "set up .lsp.json", "add go to definition", "add find references", "integrate language server protocol", or needs guidance on LSP server configuration, language server setup, or code intelligence features for Claude Code plugins.
---

# LSP Integration for Claude Code Plugins

## Overview

LSP (Language Server Protocol) plugins give Claude real-time code intelligence while working on codebases. LSP integration provides instant diagnostics, code navigation, and language awareness that enhances Claude's ability to understand and modify code.

**Key capabilities:**
- Instant diagnostics (errors and warnings after each edit)
- Code navigation (go to definition, find references)
- Hover information (type info and documentation)
- Language awareness (understanding of code symbols)

## When to Use LSP Plugins

**Use LSP plugins when:**
- Plugin works with specific programming languages
- Users need real-time error feedback
- Code navigation improves workflow
- Language-specific intelligence is valuable

**Note:** For common languages (TypeScript, Python, Rust), users should install pre-built LSP plugins from the official marketplace. Create custom LSP plugins only for languages not already covered.

## LSP Configuration

### Configuration Location

LSP servers can be configured in two ways:

**Standalone file (recommended for plugins):**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── .lsp.json              # LSP server definitions
└── ...
```

**Inline in plugin.json:**
```json
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

### Basic Configuration

**.lsp.json file format:**

```json
{
  "language-name": {
    "command": "language-server-binary",
    "args": ["arg1", "arg2"],
    "extensionToLanguage": {
      ".ext": "language-id"
    }
  }
}
```

**Example - Go language server:**

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Example - TypeScript language server:**

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    }
  }
}
```

## Configuration Fields

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `command` | LSP binary to execute (must be in PATH) | `"gopls"`, `"pyright"` |
| `extensionToLanguage` | Maps file extensions to language identifiers | `{".go": "go"}` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `args` | Command-line arguments for server | `[]` |
| `transport` | Communication transport | `"stdio"` |
| `env` | Environment variables for server | `{}` |
| `initializationOptions` | Options passed during initialization | `{}` |
| `settings` | Settings via `workspace/didChangeConfiguration` | `{}` |
| `workspaceFolder` | Workspace folder path | Project root |
| `startupTimeout` | Max startup wait time (ms) | System default |
| `shutdownTimeout` | Max shutdown wait time (ms) | System default |
| `restartOnCrash` | Auto-restart if server crashes | `false` |
| `maxRestarts` | Max restart attempts | System default |
| `loggingConfig` | Debug logging configuration | `{}` |

### Transport Options

**stdio (default):** Communication via stdin/stdout
```json
{
  "transport": "stdio"
}
```

**socket:** Communication via TCP socket
```json
{
  "transport": "socket"
}
```

## Advanced Configuration

### Environment Variables

Pass environment variables to the language server:

```json
{
  "rust": {
    "command": "rust-analyzer",
    "env": {
      "RUST_LOG": "info",
      "CARGO_HOME": "/custom/cargo/path"
    },
    "extensionToLanguage": {
      ".rs": "rust"
    }
  }
}
```

### Initialization Options

Pass options during server initialization:

```json
{
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "initializationOptions": {
      "python": {
        "analysis": {
          "typeCheckingMode": "strict"
        }
      }
    },
    "extensionToLanguage": {
      ".py": "python"
    }
  }
}
```

### Workspace Settings

Configure server behavior via settings:

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "settings": {
      "typescript": {
        "format": {
          "semicolons": "insert"
        }
      }
    },
    "extensionToLanguage": {
      ".ts": "typescript"
    }
  }
}
```

### Debug Logging

Enable verbose logging for troubleshooting (activated with `--enable-lsp-logging`):

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "loggingConfig": {
      "args": ["--log-level", "4"],
      "env": {
        "TSS_LOG": "-level verbose -file ${CLAUDE_PLUGIN_LSP_LOG_FILE}"
      }
    },
    "extensionToLanguage": {
      ".ts": "typescript"
    }
  }
}
```

**Special variable:** `${CLAUDE_PLUGIN_LSP_LOG_FILE}` expands to the log file path. Logs are written to `~/.claude/debug/`.

### Crash Recovery

Configure automatic restart on server crashes:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "restartOnCrash": true,
    "maxRestarts": 3,
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

## Common Language Servers

### Available LSP Plugins (Official Marketplace)

| Plugin | Language Server | Install Command |
|--------|-----------------|-----------------|
| `pyright-lsp` | Pyright (Python) | `pip install pyright` or `npm install -g pyright` |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | rust-analyzer | See [rust-analyzer installation](https://rust-analyzer.github.io/manual.html#installation) |

### Other Language Servers

**Go:**
```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```
Install: `go install golang.org/x/tools/gopls@latest`

**C/C++:**
```json
{
  "cpp": {
    "command": "clangd",
    "args": ["--background-index"],
    "extensionToLanguage": {
      ".c": "c",
      ".cpp": "cpp",
      ".h": "c",
      ".hpp": "cpp"
    }
  }
}
```
Install: Via system package manager or LLVM releases

**Java:**
```json
{
  "java": {
    "command": "jdtls",
    "extensionToLanguage": {
      ".java": "java"
    }
  }
}
```
Install: Eclipse JDT Language Server

**Ruby:**
```json
{
  "ruby": {
    "command": "solargraph",
    "args": ["stdio"],
    "extensionToLanguage": {
      ".rb": "ruby"
    }
  }
}
```
Install: `gem install solargraph`

## Plugin Integration

### Using ${CLAUDE_PLUGIN_ROOT}

Reference plugin-bundled language servers:

```json
{
  "custom-lang": {
    "command": "${CLAUDE_PLUGIN_ROOT}/bin/custom-lsp",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".custom": "custom-lang"
    }
  }
}
```

### Plugin Directory Structure

```
my-lsp-plugin/
├── .claude-plugin/
│   └── plugin.json
├── .lsp.json
├── bin/
│   └── custom-lsp          # Bundled language server (optional)
└── README.md
```

## User Requirements

**Important:** LSP plugins configure how Claude Code connects to language servers, but they don't include the server binaries themselves.

**Document in plugin README:**
1. Required language server binary
2. Installation command
3. Version requirements
4. PATH configuration if needed

**Example README section:**
```markdown
## Prerequisites

This plugin requires gopls (Go language server):

```bash
go install golang.org/x/tools/gopls@latest
```

Ensure `gopls` is available in your PATH.
```

## Troubleshooting

### Common Issues

**"Executable not found in $PATH":**
- Language server binary not installed
- Binary not in PATH
- Check `/plugin` Errors tab for details

**Server not starting:**
- Verify command and args are correct
- Check for required dependencies
- Test server manually: `language-server --stdio`
- Use `claude --debug` for detailed logs

**No diagnostics appearing:**
- Check `extensionToLanguage` mapping
- Verify file extension matches configuration
- Confirm server supports diagnostics

**Performance issues:**
- Adjust `startupTimeout` for slow servers
- Check server resource usage
- Consider `workspaceFolder` scope

### Debugging

Enable LSP logging:
```bash
claude --enable-lsp-logging
```

View logs in `~/.claude/debug/`.

Check plugin status:
```
/plugin
```
Navigate to Errors tab to see LSP-related issues.

## Best Practices

### Configuration

1. **Use stdio transport** unless socket is specifically required
2. **Set reasonable timeouts** for slow-starting servers
3. **Enable restartOnCrash** for production stability
4. **Document all prerequisites** clearly in README

### File Extensions

1. **Map all relevant extensions** for the language
2. **Use standard language identifiers** (match VS Code language IDs)
3. **Consider related file types** (.tsx for TypeScript React, etc.)

### Error Handling

1. **Test server installation** before plugin distribution
2. **Provide clear error messages** in documentation
3. **Include troubleshooting steps** in README
4. **Suggest fallback options** if server unavailable

### Performance

1. **Limit background indexing** for large codebases
2. **Configure appropriate settings** for your use case
3. **Test with realistic project sizes**
4. **Monitor memory usage** of language servers

## Quick Reference

### Minimal Configuration

```json
{
  "language": {
    "command": "language-server",
    "extensionToLanguage": {
      ".ext": "language-id"
    }
  }
}
```

### Full Configuration

```json
{
  "language": {
    "command": "language-server",
    "args": ["--stdio"],
    "transport": "stdio",
    "env": {
      "VAR": "value"
    },
    "initializationOptions": {},
    "settings": {},
    "workspaceFolder": "/path/to/workspace",
    "startupTimeout": 10000,
    "shutdownTimeout": 5000,
    "restartOnCrash": true,
    "maxRestarts": 3,
    "loggingConfig": {
      "args": ["--verbose"],
      "env": {}
    },
    "extensionToLanguage": {
      ".ext": "language-id"
    }
  }
}
```

## Additional Resources

### Example Configurations

See `examples/` directory for working configurations:
- `go-lsp.json` - Go language server
- `python-lsp.json` - Python with Pyright
- `multi-language.json` - Multiple language servers

### External Resources

- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [LSP Implementations](https://microsoft.github.io/language-server-protocol/implementors/servers/)
- [Claude Code Plugins Reference](/en/plugins-reference#lsp-servers)
