#!/bin/bash
# Wire up marketplace plugins for local development
# Uses version-based cache paths (9.9.9-dev) for stability

set -e

CACHE_BASE="$HOME/.claude/plugins/cache/astrosteveo-marketplace"
DEV_BASE="$HOME/workspace/marketplace/plugins"
DEV_VERSION="9.9.9-dev"

# Discover all plugins dynamically
for dev_path in "$DEV_BASE"/*/; do
    dev_path="${dev_path%/}"  # Remove trailing slash
    plugin=$(basename "$dev_path")
    cache_path="$CACHE_BASE/$plugin/$DEV_VERSION"

    if [[ -L "$cache_path" ]]; then
        echo "✓  $plugin already linked"
        continue
    fi

    if [[ -d "$cache_path" ]]; then
        echo "→  Replacing $plugin cache with symlink"
        rm -rf "$cache_path"
    else
        echo "→  Creating $plugin symlink"
        mkdir -p "$(dirname "$cache_path")"
    fi

    ln -sf "$dev_path" "$cache_path"
done

echo ""
echo "Done! Plugins linked at version $DEV_VERSION"
