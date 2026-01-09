#!/bin/bash
set -e

# Plugin-Dev Installer
# Installs skills, agents, and commands for Claude Code plugin development

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
# Derive plugin root from script location if not set
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"
DEST="${CLAUDE_PROJECT_DIR:-.}/.claude"
FORCE=false
DRY_RUN=false
QUIET=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE=true
            shift
            ;;
        --dry-run|-n)
            DRY_RUN=true
            shift
            ;;
        --quiet|-q)
            QUIET=true
            shift
            ;;
        --help|-h)
            echo "Plugin-Dev Installer"
            echo ""
            echo "Usage: init.sh [options]"
            echo ""
            echo "Options:"
            echo "  -f, --force     Overwrite existing files without prompting"
            echo "  -n, --dry-run   Show what would be installed without making changes"
            echo "  -q, --quiet     Minimal output"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Components installed:"
            echo "  Skills:   Plugin development reference skills"
            echo "  Agents:   Agent creator, plugin validator, skill reviewer"
            echo "  Commands: create-plugin workflow command"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Logging functions (all output to stderr to keep stdout clean for return values)
log_info() {
    if [[ "$QUIET" != true ]]; then
        echo -e "${BLUE}ℹ${NC} $1" >&2
    fi
}

log_success() {
    if [[ "$QUIET" != true ]]; then
        echo -e "${GREEN}✓${NC} $1" >&2
    fi
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1" >&2
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

log_header() {
    if [[ "$QUIET" != true ]]; then
        echo "" >&2
        echo -e "${BOLD}${CYAN}$1${NC}" >&2
        echo -e "${CYAN}$(printf '─%.0s' {1..50})${NC}" >&2
    fi
}

# Check if source templates exist
check_sources() {
    local missing=0

    if [[ ! -d "$PLUGIN_ROOT/templates/skills" ]]; then
        log_error "Skills templates not found at $PLUGIN_ROOT/templates/skills"
        missing=1
    fi

    if [[ ! -d "$PLUGIN_ROOT/templates/agents" ]]; then
        log_error "Agents templates not found at $PLUGIN_ROOT/templates/agents"
        missing=1
    fi

    if [[ ! -d "$PLUGIN_ROOT/templates/commands" ]]; then
        log_error "Commands templates not found at $PLUGIN_ROOT/templates/commands"
        missing=1
    fi

    if [[ $missing -eq 1 ]]; then
        log_error "Template sources missing. Is CLAUDE_PLUGIN_ROOT set correctly?"
        exit 1
    fi
}

# Detect conflicts with existing files
detect_conflicts() {
    local conflicts=()

    # Check skills
    if [[ -d "$PLUGIN_ROOT/templates/skills" ]]; then
        for skill in "$PLUGIN_ROOT/templates/skills"/*; do
            if [[ -d "$skill" ]]; then
                local name=$(basename "$skill")
                if [[ -d "$DEST/skills/$name" ]]; then
                    conflicts+=("skills/$name")
                fi
            fi
        done
    fi

    # Check agents
    if [[ -d "$PLUGIN_ROOT/templates/agents" ]]; then
        for agent in "$PLUGIN_ROOT/templates/agents"/*; do
            if [[ -f "$agent" ]]; then
                local name=$(basename "$agent")
                if [[ -f "$DEST/agents/$name" ]]; then
                    conflicts+=("agents/$name")
                fi
            fi
        done
    fi

    # Check commands
    if [[ -d "$PLUGIN_ROOT/templates/commands" ]]; then
        for cmd in "$PLUGIN_ROOT/templates/commands"/*; do
            if [[ -f "$cmd" ]]; then
                local name=$(basename "$cmd")
                if [[ -f "$DEST/commands/$name" ]]; then
                    conflicts+=("commands/$name")
                fi
            fi
        done
    fi

    echo "${conflicts[@]}"
}

# Install a component type
install_component() {
    local type=$1
    local src="$PLUGIN_ROOT/templates/$type"
    local dst="$DEST/$type"
    local count=0

    if [[ ! -d "$src" ]]; then
        return 0
    fi

    mkdir -p "$dst"

    for item in "$src"/*; do
        if [[ -e "$item" ]]; then
            local name=$(basename "$item")
            local target="$dst/$name"

            if [[ "$DRY_RUN" == true ]]; then
                if [[ -e "$target" ]]; then
                    log_info "[dry-run] Would overwrite: $type/$name"
                else
                    log_info "[dry-run] Would install: $type/$name"
                fi
            else
                cp -r "$item" "$dst/"
                log_success "Installed $type/$name"
            fi
            ((count++))
        fi
    done

    echo $count
}

# Main installation
main() {
    log_header "Plugin-Dev Installer"

    if [[ "$DRY_RUN" == true ]]; then
        log_warning "Dry run mode - no changes will be made"
    fi

    # Validate sources
    log_info "Checking template sources..."
    check_sources

    # Check for conflicts
    local conflicts
    conflicts=$(detect_conflicts)

    if [[ -n "$conflicts" && "$FORCE" != true && "$DRY_RUN" != true ]]; then
        log_warning "The following components already exist:"
        for conflict in $conflicts; do
            echo "  - $conflict" >&2
        done
        echo "" >&2
        log_info "Use --force to overwrite existing files"
        log_info "Use --dry-run to preview changes"
        exit 1
    fi

    # Create destination directory
    if [[ "$DRY_RUN" != true ]]; then
        mkdir -p "$DEST"
    fi

    # Install components
    log_header "Installing Skills"
    local skills_count
    skills_count=$(install_component "skills")

    log_header "Installing Agents"
    local agents_count
    agents_count=$(install_component "agents")

    log_header "Installing Commands"
    local commands_count
    commands_count=$(install_component "commands")

    # Summary
    log_header "Installation Summary"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "Would install $skills_count skills"
        log_info "Would install $agents_count agents"
        log_info "Would install $commands_count commands"
        log_info "Target directory: $DEST"
    else
        log_success "Installed $skills_count skills"
        log_success "Installed $agents_count agents"
        log_success "Installed $commands_count commands"
        echo "" >&2
        log_info "Location: $DEST"
        echo "" >&2
        echo -e "${GREEN}${BOLD}Plugin-Dev toolkit is ready!${NC}" >&2
        echo "" >&2
        echo "Use /create-plugin to start building a new Claude Code plugin." >&2
    fi
}

main "$@"
