# Changelog

All notable changes to the Harness marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed
- **BREAKING**: Migrated from `docs/` to `.artifacts/` structure throughout the harness plugin
  - Old: `docs/plans/YYYY-MM-DD-<topic>.md`
  - New: `.artifacts/<feature-name>/YYYY-MM-DD-<artifact-type>.md`
  - Updated all 5 core skills (brainstorming, writing-plans, executing-plans, subagent-driven-development, requesting-code-review)
  - Updated all test infrastructure (6 test scripts, 7 test prompt files)
  - Migrated existing documentation to feature-based organization
- The harness plugin's `.artifacts/` directory is now tracked in the repository (contains plugin's own design docs and research)

### Fixed
- Corrected marketplace identifier from `@harness-marketplace` to `@harness-mp` in install command

### Added
- Comprehensive marketplace README with installation instructions, plugin standards, and contributing guidelines

## [2026-01-05] - Initial Public Release

### Added
- **Harness Plugin** - Complete rebranding from agent-workflow with optimized skill descriptions
  - 14 skills following Claude Code best practices
  - All skill descriptions focus on triggering conditions
  - Improved keyword coverage for better skill discovery
  - Skills: brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-harness, verification-before-completion, writing-plans, using-git-worktrees, writing-skills

### Changed
- Rebranded from `agent-workflow` to `harness` throughout the plugin
- All skill descriptions rewritten to follow "Use when..." pattern (under 500 characters)
- Removed workflow summaries that could short-circuit reading full skills
- All descriptions written in third person for system prompt injection

## [2025-12-22] - Development Evolution

### Added
- **Explore-Plan-Implement-Commit Plugin** - Adaptive development workflow for all skill levels
  - Six focused skills: brainstorm, explore, design, plan, implement, commit
  - Adapts to user experience level (beginner → senior)
  - One question at a time throughout
  - TDD by default in all implementation tasks
  - Artifacts saved to `.workflow/NNN-feature-slug/`

### Changed
- Rebranded superpowers plugin to agent-workflow
- Added exploration skill for codebase understanding + external research
- Updated workflow: exploration → brainstorming → planning → implementation
- Removed old agile-workflow directory

### Removed
- Removed plugin-dev plugin (functionality consolidated)
- Removed obsolete agent-workflow-dev marketplace configuration

## [2025-12-21] - Workflow Refinement

### Added
- Discovery, implementation, and planning skills with detailed processes and templates
  - `discovery` skill: Socratic dialogue for design validation
  - `implement` skill: Execute plans with fresh agent per task
  - `plan` skill: Transform designs into actionable implementation plans
- Prompt templates for implementers, spec reviewers, and quality reviewers
- Tests and scaffolding for subagent-driven development projects

### Changed
- Major refactor based on ACE-FCA (Advanced Context Engineering) research
- Simplified to Research → Plan → Implement workflow
- Dropped PRD/epic/story hierarchy for simpler, more effective workflow
- New artifact structure: `docs/project.md`, `docs/research/`, `docs/plans/`
- Philosophy: "Human effort on plan review, not code review"

### Removed
- Removed discovery, explore, plan agents (replaced by skills)
- Removed old PRD/state.json reference files

## [2025-12-20] - Enhanced Workflow & OSS Support

### Added
- **Agile-Workflow Plugin** - Initial plugin enforcing AGILE-style project management
  - Socratic discovery with one question at a time
  - TDD with bite-sized tasks (2-5 minutes each)
  - Subagent-driven development pattern
  - Fresh implementer subagent per task
  - Two-stage review: spec compliance then quality
- New skills: subagent-driven-development, systematic-debugging, verification-before-completion, spec-compliance-review, code-quality-review, git-worktrees, finishing-branch
- **Agent-Toolkit Plugin** - Templates and best practices for creating Claude Code subagents
- OSS contribution support: respects project conventions, GitHub issues as requirements source, adapts commit messages
- Marketplace manifest for plugin distribution

### Changed
- Restructured repository to support multiple plugins
- Applied subagent creation best practices to all workflow agents
- Adopted superpowers pattern for subagent-driven-development

### Fixed
- Corrected tools format in agent templates (comma-separated, not JSON array)
- Fixed plugin-dev validation patterns to match official Claude Code documentation
- Added Write tool to explore agent

## Project Origins

### Vision Documents (2025-12-20)
- AGILE workflow plugin vision: Enforces AGILE-style project management optimized for LLM context limitations
- PRD defining five epics: project-scaffold, agent-definitions, workflow-orchestration, state-management, commands-and-skills
- /workflow command design with context-aware routing
- Git-first principle: auto-init repo, automatic commits at workflow points
- Fibonacci story point effort tracking

---

## Attribution

The Harness plugin is based on [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent (obra).

## Philosophy

- **YAGNI** (You Aren't Gonna Need It) - Build only what's needed now
- **TDD** (Test-Driven Development) - Write tests first, code second
- **Systematic approaches** - Disciplined processes prevent preventable mistakes
- **1% threshold rule** - If there's even a 1% chance a skill applies, use it

## Support

- Report issues: [GitHub Issues](https://github.com/astrosteveo/harness-mp/issues)
- Sponsor development: [GitHub Sponsors](https://github.com/sponsors/astrosteveo)
