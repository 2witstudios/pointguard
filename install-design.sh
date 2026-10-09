#!/bin/zsh
# Install the shared design skill and agent-specific invocation wrappers.
set -euo pipefail

REPO="${0:A:h}"
CODEX_TARGET="${CODEX_HOME:-$HOME/.codex}"
OPENCODE_TARGET="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
SOURCES=(
  "$REPO/skills/design"
  "$REPO/skills/design"
  "$REPO/commands/design.md"
  "$REPO/commands/design.md"
  "$REPO/commands/design.md"
)
DESTINATIONS=(
  "$HOME/.agents/skills/design"
  "$OPENCODE_TARGET/skills/design"
  "$HOME/.claude/commands/pg/design.md"
  "$OPENCODE_TARGET/commands/design.md"
  "$CODEX_TARGET/prompts/design.md"
)

# Preflight every destination. Never replace an unrelated skill or command.
for (( i=1; i<=${#SOURCES}; i++ )); do
  source="${SOURCES[$i]}"
  dest="${DESTINATIONS[$i]}"
  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ -L "$dest" && "${dest:A}" == "${source:A}" ]]; then
      continue
    fi
    print -u2 "Refusing to replace existing design entry: $dest"
    exit 1
  fi
done

for (( i=1; i<=${#SOURCES}; i++ )); do
  source="${SOURCES[$i]}"
  dest="${DESTINATIONS[$i]}"
  if [[ ! -e "$dest" && ! -L "$dest" ]]; then
    mkdir -p "${dest:h}"
    ln -s "$source" "$dest"
    print "linked $dest -> $source"
  fi
done
