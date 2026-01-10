---
name: hook-development
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostToolUse/Stop hook", "validate tool use", "implement prompt-based hooks", "use ${CLAUDE_PLUGIN_ROOT}", "set up event-driven automation", "block dangerous commands", or mentions hook events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, Stop, SubagentStart, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification). Provides comprehensive guidance for creating and implementing Claude Code plugin hooks with focus on advanced prompt-based hooks API.
---

# Hook Development for Claude Code Plugins

## Overview

Hooks are event-driven automation scripts that execute in response to Claude Code events. Use hooks to validate operations, enforce policies, add context, and integrate external tools into workflows.

**Key capabilities:**
- Validate tool calls before execution (PreToolUse)
- React to tool results (PostToolUse)
- Enforce completion standards (Stop, SubagentStop)
- Load project context (SessionStart)
- Automate workflows across the development lifecycle

## Hook Types

### Prompt-Based Hooks (Recommended)

Use LLM-driven decision making for context-aware validation:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

**Supported events:** Stop, SubagentStop, UserPromptSubmit, PreToolUse

**Benefits:**
- Context-aware decisions based on natural language reasoning
- Flexible evaluation logic without bash scripting
- Better edge case handling
- Easier to maintain and extend

### Command Hooks

Execute bash commands for deterministic checks:

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**Use for:**
- Fast deterministic validations
- File system operations
- External tool integrations
- Performance-critical checks

### Hook Options

#### timeout (optional)

How long a hook should run before canceling. Specified in seconds.

**Defaults:** Command hooks (60s), Prompt hooks (30s)

#### once (optional)

Set to `true` to run the hook only once per session. After the first successful execution, the hook is removed.

**Note:** This option is only supported for hooks defined in skills and slash commands, not for agents or settings-based hooks.

```json
{
  "type": "command",
  "command": "./scripts/one-time-setup.sh",
  "once": true
}
```

**Use cases:**
- One-time validation at start of skill execution
- Initial setup that shouldn't repeat
- Resource-intensive checks that only need to run once

## Hook Configuration Formats

### Plugin hooks.json Format

**For plugin hooks** in `hooks/hooks.json`, use wrapper format:

```json
{
  "description": "Brief explanation of hooks (optional)",
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

**Key points:**
- `description` field is optional
- `hooks` field is required wrapper containing actual hook events
- This is the **plugin-specific format**

**Example:**
```json
{
  "description": "Validation hooks for code quality",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### Settings Format (Direct)

**For user settings** in `.claude/settings.json`, use direct format:

```json
{
  "PreToolUse": [...],
  "Stop": [...],
  "SessionStart": [...]
}
```

**Key points:**
- No wrapper - events directly at top level
- No description field
- This is the **settings format**

**Important:** The examples below show the hook event structure that goes inside either format. For plugin hooks.json, wrap these in `{"hooks": {...}}`.

## Hook Events

### PreToolUse

Execute before any tool runs. Use to approve, deny, or modify tool calls.

**Example (prompt-based):**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety. Check: system paths, credentials, path traversal, sensitive content. Return 'approve' or 'deny'."
        }
      ]
    }
  ]
}
```

**Output for PreToolUse:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

### PostToolUse

Execute after tool completes successfully. Use to react to results, provide feedback, or log.

**Example:**
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze edit result for potential issues: syntax errors, security vulnerabilities, breaking changes. Provide feedback."
        }
      ]
    }
  ]
}
```

**Output behavior:**
- Exit 0: stdout shown in transcript
- Exit 2: stderr fed back to Claude
- systemMessage included in context

### PostToolUseFailure

Execute after tool execution fails. Use to handle errors, provide recovery suggestions, or log failures.

**Example:**
```json
{
  "PostToolUseFailure": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze the command failure and suggest fixes or alternative approaches."
        }
      ]
    }
  ]
}
```

### PermissionRequest

Execute when a permission dialog is shown to the user. Use to automatically allow or deny permissions based on rules.

**Example:**
```json
{
  "PermissionRequest": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-permission.sh"
        }
      ]
    }
  ]
}
```

Recognizes the same matcher values as PreToolUse.

### Stop

Execute when main agent considers stopping. Use to validate completeness.

**Example:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion: tests run, build succeeded, questions answered. Return 'approve' to stop or 'block' with reason to continue."
        }
      ]
    }
  ]
}
```

**Decision output:**
```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

### SubagentStart

Execute when a subagent is started. Use to configure subagent behavior or log subagent invocations.

**Example:**
```json
{
  "SubagentStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/log-subagent.sh"
        }
      ]
    }
  ]
}
```

### SubagentStop

Execute when subagent considers stopping. Use to ensure subagent completed its task.

Similar to Stop hook, but for subagents.

### UserPromptSubmit

Execute when user submits a prompt. Use to add context, validate, or block prompts.

**Example:**
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Check if prompt requires security guidance. If discussing auth, permissions, or API security, return relevant warnings."
        }
      ]
    }
  ]
}
```

### SessionStart

Execute when Claude Code session begins. Use to load context and set environment.

**Matchers:**
- `startup` - Normal startup
- `resume` - Invoked from `--resume`, `--continue`, or `/resume`
- `clear` - Invoked from `/clear`
- `compact` - Invoked from auto or manual compact

**Example:**
```json
{
  "SessionStart": [
    {
      "matcher": "startup",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

**Special capability:** Persist environment variables using `$CLAUDE_ENV_FILE`:
```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

See `examples/load-context.sh` for complete example.

### SessionEnd

Execute when session ends. Use for cleanup, logging, and state preservation.

The `reason` field in hook input will be one of: `clear`, `logout`, `prompt_input_exit`, `other`.

### PreCompact

Execute before context compaction. Use to add critical information to preserve.

**Matchers:**
- `manual` - Invoked from `/compact`
- `auto` - Invoked from auto-compact (due to full context window)

### Notification

Execute when Claude sends notifications. Use to react to user notifications.

**Matchers:**
- `permission_prompt` - Permission requests from Claude Code
- `idle_prompt` - When Claude is waiting for user input (after 60+ seconds idle)
- `auth_success` - Authentication success notifications
- `elicitation_dialog` - When Claude Code needs input for MCP tool elicitation

**Example:**
```json
{
  "Notification": [
    {
      "matcher": "permission_prompt",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/notify-permission.sh"
        }
      ]
    }
  ]
}
```

## Hook Output Format

### Standard Output (All Hooks)

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

- `continue`: If false, halt processing (default true)
- `suppressOutput`: Hide output from transcript (default false)
- `systemMessage`: Message shown to Claude

### Exit Codes

- `0` - Success (stdout shown in transcript)
- `2` - Blocking error (stderr fed back to Claude)
- Other - Non-blocking error

## Hook Input Format

All hooks receive JSON via stdin with common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

**Event-specific fields:**

- **PreToolUse/PostToolUse:** `tool_name`, `tool_input`, `tool_result`
- **UserPromptSubmit:** `user_prompt`
- **Stop/SubagentStop:** `reason`

Access fields in prompts using `$TOOL_INPUT`, `$TOOL_RESULT`, `$USER_PROMPT`, etc.

## Environment Variables

Available in all command hooks:

### Core Variables

- **`$CLAUDE_PROJECT_DIR`** - Absolute path to the project root directory (where Claude Code was started). Use this to reference project files in a portable way.

- **`$CLAUDE_PLUGIN_ROOT`** - Absolute path to the plugin directory. **Essential for plugin hooks** - always use this instead of hardcoded paths to ensure hooks work regardless of where the plugin is installed.

### Special Variables

- **`$CLAUDE_ENV_FILE`** - (SessionStart only) File path where you can persist environment variables for subsequent bash commands. Write `export VAR=value` lines to this file:
  ```bash
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-key' >> "$CLAUDE_ENV_FILE"
  ```

- **`$CLAUDE_CODE_REMOTE`** - Set to `"true"` if running in remote (web) environment, not set or empty for local CLI. Use to run different logic based on execution context:
  ```bash
  if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
    # Remote-specific logic
  else
    # Local CLI logic
  fi
  ```

### Usage Examples

**Always use ${CLAUDE_PLUGIN_ROOT} in plugin hook commands for portability:**

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

**Reference project files with ${CLAUDE_PROJECT_DIR}:**

```json
{
  "type": "command",
  "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
}
```

## Plugin Hook Configuration

In plugins, define hooks in `hooks/hooks.json`:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion"
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

Plugin hooks merge with user's hooks and run in parallel.

## Matchers

### Tool Name Matching

**Exact match:**
```json
"matcher": "Write"
```

**Multiple tools:**
```json
"matcher": "Read|Write|Edit"
```

**Wildcard (all tools):**
```json
"matcher": "*"
```

**Regex patterns:**
```json
"matcher": "mcp__.*__delete.*"  // All MCP delete tools
```

**Note:** Matchers are case-sensitive.

### Common Patterns

```json
// All MCP tools
"matcher": "mcp__.*"

// Specific plugin's MCP tools
"matcher": "mcp__plugin_asana_.*"

// All file operations
"matcher": "Read|Write|Edit"

// Bash commands only
"matcher": "Bash"
```

## Security Best Practices

### Input Validation

Always validate inputs in command hooks:

```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# Validate tool name format
if [[ ! "$tool_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo '{"decision": "deny", "reason": "Invalid tool name"}' >&2
  exit 2
fi
```

### Path Safety

Check for path traversal and sensitive files:

```bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Deny path traversal
if [[ "$file_path" == *".."* ]]; then
  echo '{"decision": "deny", "reason": "Path traversal detected"}' >&2
  exit 2
fi

# Deny sensitive files
if [[ "$file_path" == *".env"* ]]; then
  echo '{"decision": "deny", "reason": "Sensitive file"}' >&2
  exit 2
fi
```

See `examples/validate-write.sh` and `examples/validate-bash.sh` for complete examples.

### Quote All Variables

```bash
# GOOD: Quoted
echo "$file_path"
cd "$CLAUDE_PROJECT_DIR"

# BAD: Unquoted (injection risk)
echo $file_path
cd $CLAUDE_PROJECT_DIR
```

### Set Appropriate Timeouts

```json
{
  "type": "command",
  "command": "bash script.sh",
  "timeout": 10
}
```

**Defaults:** Command hooks (60s), Prompt hooks (30s)

## Performance Considerations

### Parallel Execution

All matching hooks run **in parallel**:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {"type": "command", "command": "check1.sh"},  // Parallel
        {"type": "command", "command": "check2.sh"},  // Parallel
        {"type": "prompt", "prompt": "Validate..."}   // Parallel
      ]
    }
  ]
}
```

**Design implications:**
- Hooks don't see each other's output
- Non-deterministic ordering
- Design for independence

### Optimization

1. Use command hooks for quick deterministic checks
2. Use prompt hooks for complex reasoning
3. Cache validation results in temp files
4. Minimize I/O in hot paths

## Temporarily Active Hooks

Create hooks that activate conditionally by checking for a flag file or configuration:

**Pattern: Flag file activation**
```bash
#!/bin/bash
# Only active when flag file exists
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"

if [ ! -f "$FLAG_FILE" ]; then
  # Flag not present, skip validation
  exit 0
fi

# Flag present, run validation
input=$(cat)
# ... validation logic ...
```

**Pattern: Configuration-based activation**
```bash
#!/bin/bash
# Check configuration for activation
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/plugin-config.json"

if [ -f "$CONFIG_FILE" ]; then
  enabled=$(jq -r '.strictMode // false' "$CONFIG_FILE")
  if [ "$enabled" != "true" ]; then
    exit 0  # Not enabled, skip
  fi
fi

# Enabled, run hook logic
input=$(cat)
# ... hook logic ...
```

**Use cases:**
- Enable strict validation only when needed
- Temporary debugging hooks
- Project-specific hook behavior
- Feature flags for hooks

**Best practice:** Document activation mechanism in plugin README so users know how to enable/disable temporary hooks.

## Hook Lifecycle and Limitations

### Hooks Load at Session Start

**Important:** Hooks are loaded when Claude Code session starts. Changes to hook configuration require restarting Claude Code.

**Cannot hot-swap hooks:**
- Editing `hooks/hooks.json` won't affect current session
- Adding new hook scripts won't be recognized
- Changing hook commands/prompts won't update
- Must restart Claude Code: exit and run `claude` again

**To test hook changes:**
1. Edit hook configuration or scripts
2. Exit Claude Code session
3. Restart: `claude` or `cc`
4. New hook configuration loads
5. Test hooks with `claude --debug`

### Hook Validation at Startup

Hooks are validated when Claude Code starts:
- Invalid JSON in hooks.json causes loading failure
- Missing scripts cause warnings
- Syntax errors reported in debug mode

Use `/hooks` command to review loaded hooks in current session.

## Debugging Hooks

### Enable Debug Mode

```bash
claude --debug
```

Look for hook registration, execution logs, input/output JSON, and timing information.

### Test Hook Scripts

Test command hooks directly:

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "/test"}}' | \
  bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh

echo "Exit code: $?"
```

### Validate JSON Output

Ensure hooks output valid JSON:

```bash
output=$(./your-hook.sh < test-input.json)
echo "$output" | jq .
```

## Quick Reference

### Hook Events Summary

| Event | When | Use For |
|-------|------|---------|
| PreToolUse | Before tool | Validation, modification |
| PostToolUse | After tool succeeds | Feedback, logging |
| PostToolUseFailure | After tool fails | Error handling, recovery |
| PermissionRequest | Permission dialog shown | Auto-allow/deny |
| UserPromptSubmit | User input | Context, validation |
| Stop | Agent stopping | Completeness check |
| SubagentStart | Subagent begins | Configuration, logging |
| SubagentStop | Subagent done | Task validation |
| SessionStart | Session begins | Context loading |
| SessionEnd | Session ends | Cleanup, logging |
| PreCompact | Before compact | Preserve context |
| Notification | User notified | Logging, reactions |

### Best Practices

**DO:**
- ✅ Use prompt-based hooks for complex logic
- ✅ Use ${CLAUDE_PLUGIN_ROOT} for portability
- ✅ Validate all inputs in command hooks
- ✅ Quote all bash variables
- ✅ Set appropriate timeouts
- ✅ Return structured JSON output
- ✅ Test hooks thoroughly

**DON'T:**
- ❌ Use hardcoded paths
- ❌ Trust user input without validation
- ❌ Create long-running hooks
- ❌ Rely on hook execution order
- ❌ Modify global state unpredictably
- ❌ Log sensitive information

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:

- **`references/patterns.md`** - Common hook patterns (8+ proven patterns)
- **`references/migration.md`** - Migrating from basic to advanced hooks
- **`references/advanced.md`** - Advanced use cases and techniques

### Example Hook Scripts

Working examples in `examples/`:

- **`validate-write.sh`** - File write validation example
- **`validate-bash.sh`** - Bash command validation example
- **`load-context.sh`** - SessionStart context loading example

### Utility Scripts

Development tools in `scripts/`:

- **`validate-hook-schema.sh`** - Validate hooks.json structure and syntax
- **`test-hook.sh`** - Test hooks with sample input before deployment
- **`hook-linter.sh`** - Check hook scripts for common issues and best practices

### External Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code/hooks
- **Examples**: See security-guidance plugin in marketplace
- **Testing**: Use `claude --debug` for detailed logs
- **Validation**: Use `jq` to validate hook JSON output

## Implementation Workflow

To implement hooks in a plugin:

1. Identify events to hook into (PreToolUse, Stop, SessionStart, etc.)
2. Decide between prompt-based (flexible) or command (deterministic) hooks
3. Write hook configuration in `hooks/hooks.json`
4. For command hooks, create hook scripts
5. Use ${CLAUDE_PLUGIN_ROOT} for all file references
6. Validate configuration with `scripts/validate-hook-schema.sh hooks/hooks.json`
7. Test hooks with `scripts/test-hook.sh` before deployment
8. Test in Claude Code with `claude --debug`
9. Document hooks in plugin README

Focus on prompt-based hooks for most use cases. Reserve command hooks for performance-critical or deterministic checks.
