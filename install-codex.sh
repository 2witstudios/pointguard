#!/bin/zsh
# Install Codex-only skills and custom prompts. Leaves other agents untouched.
set -euo pipefail

REPO="${0:A:h}"
CODEX_TARGET="${CODEX_HOME:-$HOME/.codex}"

# Check every destination before making changes; preserve existing installs.
SOURCES=("$REPO"/codex-skills/*(/) "$REPO"/codex-prompts/*.md(N))
for source in $SOURCES; do
  if [[ -d "$source" ]]; then
    dest="$CODEX_TARGET/skills/${source:t}"
  else
    dest="$CODEX_TARGET/prompts/${source:t}"
  fi
  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ -L "$dest" && "${dest:A}" == "${source:A}" ]]; then
      continue
    fi
    print -u2 "Refusing to replace existing Codex entry: $dest"
    exit 1
  fi
done

mkdir -p "$CODEX_TARGET/skills" "$CODEX_TARGET/prompts"
for source in $SOURCES; do
  if [[ -d "$source" ]]; then
    dest="$CODEX_TARGET/skills/${source:t}"
  else
    dest="$CODEX_TARGET/prompts/${source:t}"
  fi
  if [[ ! -e "$dest" && ! -L "$dest" ]]; then
    ln -s "$source" "$dest"
    print "linked $dest -> $source"
  fi
done
