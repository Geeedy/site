#!/usr/bin/env bash
# Pull latest site from GitHub if the remote is ahead, then optionally rebuild pages.
# Env (optional):
#   SITE_ROOT     — repo directory (default: parent of deploy/)
#   SITE_REPO     — https://github.com/Geeedy/site.git
#   SITE_REMOTE   — origin
#   SITE_BRANCH   — main
#   SITE_FORCE_SYNC=1 — git reset --hard to remote (for production only)
#   SITE_REBUILD=1    — run tools/build_pages.py after update (default 1)
#   BASE, NOINDEX, SITE — passed through to build_pages.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SITE_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
REPO_URL="${SITE_REPO:-https://github.com/Geeedy/site.git}"
REMOTE="${SITE_REMOTE:-origin}"
BRANCH="${SITE_BRANCH:-main}"
REBUILD="${SITE_REBUILD:-1}"
FORCE="${SITE_FORCE_SYNC:-0}"

cd "$ROOT"

# Allow service user to use a repo that was synced from another UID
git config --global --add safe.directory "$ROOT" 2>/dev/null || true

if [[ ! -d .git ]]; then
  echo "ERROR: $ROOT is not a git repository" >&2
  exit 1
fi

# Ensure remote URL matches the canonical repo
if git remote get-url "$REMOTE" >/dev/null 2>&1; then
  git remote set-url "$REMOTE" "$REPO_URL"
else
  git remote add "$REMOTE" "$REPO_URL"
fi

echo "[skilldev] fetching $REMOTE/$BRANCH …"
git fetch --prune "$REMOTE" "$BRANCH"

LOCAL="$(git rev-parse HEAD)"
REMOTE_SHA="$(git rev-parse "$REMOTE/$BRANCH")"

if [[ "$LOCAL" == "$REMOTE_SHA" ]]; then
  echo "[skilldev] already up to date ($LOCAL)"
else
  echo "[skilldev] update available: ${LOCAL:0:7} → ${REMOTE_SHA:0:7}"
  if [[ "$FORCE" == "1" ]]; then
    git checkout "$BRANCH"
    git reset --hard "$REMOTE/$BRANCH"
  else
    git checkout "$BRANCH"
    git pull --ff-only "$REMOTE" "$BRANCH"
  fi
  echo "[skilldev] updated to $(git rev-parse --short HEAD)"
fi

if [[ "$REBUILD" == "1" ]]; then
  echo "[skilldev] rebuilding pages…"
  export BASE="${BASE:-}"
  export NOINDEX="${NOINDEX:-0}"
  export SITE="${SITE:-${SITE_URL:-https://skill-dev.ai}}"
  python3 "$ROOT/tools/build_pages.py"
fi

echo "[skilldev] git update done"
