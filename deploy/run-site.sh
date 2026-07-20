#!/usr/bin/env bash
# Site entrypoint for systemd: update from GitHub, then serve.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SITE_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
export SITE_ROOT="$ROOT"

# Defaults for production-style serve (override via /etc/skilldev-site.env)
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8080}"
export BASE="${BASE:-}"

"$SCRIPT_DIR/git-update.sh"

exec python3 "$ROOT/tools/serve_i18n.py"
