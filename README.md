# Harness Marketplace

**Harnessing the full power of Claude Code**

A curated collection of Claude Code plugins for structured software development workflows.

## What is Harness?

Harness is an ecosystem of tools, workflows, and skills designed to help you get the most out of Claude Code. The marketplace provides production-ready plugins that implement battle-tested development practices through Claude's skills system.

## Available Plugins

### 🎯 harness - Complete Development Workflow

A comprehensive software development workflow built on composable skills that guide Claude through systematic brainstorming, planning, implementation, testing, and code review.

**Key Features:**
- Interactive design refinement before writing code
- Detailed implementation plans with bite-sized tasks
- Test-driven development enforcement (RED-GREEN-REFACTOR)
- Systematic debugging with root cause analysis
- Subagent-driven development with two-stage review
- Git worktree management for isolated workspaces
- Automated code review integration

**Install:**
```bash
/plugin marketplace add astrosteveo/harness-mp
/plugin install harness@harness-marketplace
```

**Learn more:** [plugins/harness/README.md](plugins/harness/README.md)

## Why Use a Marketplace?

Marketplaces allow you to:
- **Discover** vetted plugins from trusted sources
- **Install** with a single command
- **Update** automatically when improvements are released
- **Share** your own plugins with the community

## Installation

### Add This Marketplace

```bash
/plugin marketplace add astrosteveo/harness-mp
```

### List Available Plugins

```bash
/plugin marketplace list
```

### Install a Plugin

```bash
/plugin install <plugin-name>@harness-marketplace
```

### Update All Plugins

```bash
/plugin update --all
```

## Philosophy

The Harness ecosystem is built on these principles:

- **YAGNI** - You Aren't Gonna Need It (don't add complexity prematurely)
- **TDD First** - Write tests before implementation, always
- **Systematic over Ad-hoc** - Follow proven processes over guessing
- **Evidence over Claims** - Verify before declaring success
- **Skills, not Scripts** - Teach Claude patterns, don't force behavior

## Contributing

We welcome high-quality plugins that follow Harness philosophy.

### Submitting a Plugin

1. Fork this repository
2. Create `plugins/your-plugin-name/` following the structure in `plugins/harness/`
3. Add entry to `.claude-plugin/marketplace.json`
4. Submit a PR with:
   - Clear description of what the plugin does
   - Installation instructions
   - Test evidence showing it works
   - Documentation following the template

### Plugin Standards

All plugins in this marketplace must:
- Include comprehensive README.md
- Follow Claude Code skill best practices
- Be tested before submission
- Have clear, accurate skill descriptions
- Include LICENSE file
- Maintain YAGNI philosophy

See [plugins/harness/skills/writing-skills/SKILL.md](plugins/harness/skills/writing-skills/SKILL.md) for skill authoring guidance.

## Support

- **Issues**: [github.com/astrosteveo/harness-mp/issues](https://github.com/astrosteveo/harness-mp/issues)
- **Discussions**: Start a discussion in the Issues tab
- **Blog**: [blog.fsck.com](https://blog.fsck.com) (coming soon)

## Sponsorship

If Harness has helped you build something valuable, consider [sponsoring this work](https://github.com/sponsors/astrosteveo).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Attribution

The harness plugin is forked from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent, with significant enhancements and optimizations.

---

**Happy Harnessing! 🚀**
