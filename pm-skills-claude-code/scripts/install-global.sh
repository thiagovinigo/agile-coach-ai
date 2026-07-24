#!/usr/bin/env bash
# install-global.sh — Install PM skills globally for Claude Code
# Works on macOS, Linux, and WSL

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SOURCE_DIR="$REPO_DIR/.claude/commands"
TARGET_DIR="$HOME/.claude/commands"

echo "================================================"
echo "  PM Skills for Claude Code — Global Installer"
echo "================================================"
echo ""
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Check source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory not found: $SOURCE_DIR"
    echo "Make sure you're running this from the repo root or scripts/ directory."
    exit 1
fi

# Count files
FILE_COUNT=$(ls "$SOURCE_DIR"/*.md 2>/dev/null | wc -l)
echo "Found $FILE_COUNT skill files to install."
echo ""

# Warn about overwrites
if [ -d "$TARGET_DIR" ]; then
    EXISTING=$(ls "$TARGET_DIR"/*.md 2>/dev/null | wc -l)
    if [ "$EXISTING" -gt 0 ]; then
        echo "WARNING: $TARGET_DIR already contains $EXISTING .md files."
        echo "Files with the same name will be OVERWRITTEN."
        echo ""
        read -p "Continue? (y/N) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 0
        fi
    fi
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy files
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"

echo ""
echo "Done! $FILE_COUNT PM skills installed globally."
echo ""
echo "You can now use /persona, /prd, /discovery, etc. in any project."
echo "Open Claude Code in any directory to start using them."
