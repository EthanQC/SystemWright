#!/usr/bin/env sh
# Install the SystemWright Agent Skill into a host's skills directory.
# Portable POSIX sh: no bashisms, no hardcoded home, no destructive globs.
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

# Locate the skill directory: the single child of the repo root that holds a
# SKILL.md. Derived, not hardcoded, so a future rename needs no edit here.
SKILL_SRC=""
for d in "$REPO_ROOT"/*/; do
  if [ -f "${d}SKILL.md" ]; then
    SKILL_SRC=${d%/}
    break
  fi
done
if [ -z "$SKILL_SRC" ]; then
  echo "error: no skill directory (containing SKILL.md) found under $REPO_ROOT" >&2
  exit 1
fi
SKILL_NAME=$(basename "$SKILL_SRC")

usage() {
  cat <<EOF
Install the "$SKILL_NAME" Agent Skill into a host's skills directory.

usage: sh scripts/install.sh [--host <host>] [--dir <path>] [--project]

  --host <host>   one of: claude | codex | gemini | cursor
  --dir  <path>   install into a custom skills directory (used verbatim)
  --project       install into the current repo's project-level skills dir
                  for the chosen host, instead of the user-level one

Per-host user-level skills directories:
  claude  -> \$HOME/.claude/skills
  codex   -> \${CODEX_HOME:-\$HOME/.codex}/skills
  gemini  -> \$HOME/.gemini/skills
  cursor  -> \$HOME/.cursor/skills

Kimi (Moonshot) and GLM (Zhipu) run *inside* Claude Code via an
Anthropic-compatible endpoint, so install with --host claude (see README).
Windows: run under Git Bash / WSL, or copy the "$SKILL_NAME" folder into the
host's skills directory under %USERPROFILE% manually (see README).
EOF
}

HOST=""
CUSTOM_DIR=""
PROJECT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --host) HOST=${2:-}; shift 2 ;;
    --dir) CUSTOM_DIR=${2:-}; shift 2 ;;
    --project) PROJECT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

resolve_base() {
  case "$1" in
    claude) [ "$2" = 1 ] && printf '%s' "$PWD/.claude/skills" || printf '%s' "$HOME/.claude/skills" ;;
    codex)  [ "$2" = 1 ] && printf '%s' "$PWD/.agents/skills" || printf '%s' "${CODEX_HOME:-$HOME/.codex}/skills" ;;
    gemini) [ "$2" = 1 ] && printf '%s' "$PWD/.gemini/skills" || printf '%s' "$HOME/.gemini/skills" ;;
    cursor) [ "$2" = 1 ] && printf '%s' "$PWD/.cursor/skills" || printf '%s' "$HOME/.cursor/skills" ;;
    *) return 1 ;;
  esac
}

if [ -n "$CUSTOM_DIR" ]; then
  DEST_BASE=$CUSTOM_DIR
elif [ -n "$HOST" ]; then
  DEST_BASE=$(resolve_base "$HOST" "$PROJECT") || {
    echo "error: unknown host: $HOST" >&2
    usage
    exit 2
  }
else
  usage
  exit 2
fi

DEST="$DEST_BASE/$SKILL_NAME"
mkdir -p -- "$DEST_BASE"
rm -rf -- "$DEST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "$SKILL_SRC"/ "$DEST"/
else
  cp -R "$SKILL_SRC" "$DEST"
fi
echo "Installed '$SKILL_NAME' -> $DEST"

if command -v python3 >/dev/null 2>&1; then
  python3 "$SCRIPT_DIR/validate_skill.py" "$DEST" || {
    echo "warning: the installed skill failed validation" >&2
    exit 1
  }
fi
