#!/usr/bin/env bash
# Install as a systemd --user service (no root required).
# Survives reboot if lingering is enabled: loginctl enable-linger "$USER"
#
# Usage:
#   bash deploy/install-user-service.sh
#   bash deploy/install-user-service.sh "$HOME/skilldev-site"

set -euo pipefail

REPO_URL="https://github.com/Geeedy/site.git"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
SITE_ROOT="${1:-$HOME/skilldev-site}"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
ENV_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/skilldev-site.env"

mkdir -p "$UNIT_DIR" "$(dirname "$SITE_ROOT")" "$(dirname "$ENV_FILE")"

if [[ -d "$SITE_ROOT/.git" ]]; then
  echo "[install] updating $SITE_ROOT"
  git -C "$SITE_ROOT" remote set-url origin "$REPO_URL"
  git -C "$SITE_ROOT" fetch --prune origin main
  git -C "$SITE_ROOT" checkout main
  git -C "$SITE_ROOT" reset --hard origin/main
elif [[ "$SITE_ROOT" == "$SRC_REPO" ]]; then
  echo "[install] using current tree: $SITE_ROOT (no hard reset)"
else
  echo "[install] cloning → $SITE_ROOT"
  git clone --branch main "$REPO_URL" "$SITE_ROOT"
fi

chmod +x "$SITE_ROOT/deploy/"*.sh 2>/dev/null || true

# If this tree was cloned before deploy scripts were pushed, copy them from the installer source
if [[ ! -x "$SITE_ROOT/deploy/run-site.sh" ]]; then
  echo "[install] seeding deploy scripts from $SRC_REPO"
  mkdir -p "$SITE_ROOT/deploy"
  cp -a "$SRC_REPO/deploy/git-update.sh" "$SRC_REPO/deploy/run-site.sh" \
        "$SRC_REPO/deploy/skilldev-site.service" "$SRC_REPO/deploy/skilldev-site.env.example" \
        "$SRC_REPO/deploy/install-service.sh" "$SRC_REPO/deploy/install-user-service.sh" \
        "$SRC_REPO/deploy/nginx-lang.conf.example" \
        "$SITE_ROOT/deploy/" 2>/dev/null || true
  # serve script is required
  cp -a "$SRC_REPO/tools/serve_i18n.py" "$SITE_ROOT/tools/" 2>/dev/null || true
  chmod +x "$SITE_ROOT/deploy/"*.sh
fi

if [[ ! -x "$SITE_ROOT/deploy/run-site.sh" ]]; then
  echo "ERROR: deploy/run-site.sh missing in $SITE_ROOT — push deploy/ to GitHub or install from a full tree" >&2
  exit 1
fi

# User env: no force-sync if using the Cursor working copy
if [[ "$SITE_ROOT" == "$SRC_REPO" ]]; then
  FORCE=0
else
  FORCE=1
fi

cat > "$ENV_FILE" <<EOF
SITE_ROOT=$SITE_ROOT
SITE_REPO=$REPO_URL
SITE_BRANCH=main
SITE_REMOTE=origin
SITE_FORCE_SYNC=$FORCE
SITE_REBUILD=1
BASE=
NOINDEX=0
SITE=https://skill-dev.ai
SITE_URL=https://skill-dev.ai
HOST=127.0.0.1
PORT=8080
EOF

cat > "$UNIT_DIR/skilldev-site.service" <<EOF
[Unit]
Description=Skill Dev website (git sync + HTTP)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=-$ENV_FILE
WorkingDirectory=$SITE_ROOT
ExecStart=$SITE_ROOT/deploy/run-site.sh
Restart=on-failure
RestartSec=5
TimeoutStartSec=300

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable skilldev-site.service
systemctl --user restart skilldev-site.service
systemctl --user --no-pager --full status skilldev-site.service || true

echo
echo "[install] user service installed."
echo "  After reboot, enable lingering so it starts without login:"
echo "    loginctl enable-linger $USER"
echo "  Logs: journalctl --user -u skilldev-site -f"
echo "  URL:  http://127.0.0.1:8080/"
