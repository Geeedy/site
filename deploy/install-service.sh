#!/usr/bin/env bash
# Install Skill Dev site as a systemd service.
#
# Usage (as root):
#   sudo bash deploy/install-service.sh
#   sudo bash deploy/install-service.sh /var/www/skilldev-site
#
# What it does:
#   1) Clones https://github.com/Geeedy/site into SITE_ROOT (or updates it)
#   2) Writes /etc/skilldev-site.env
#   3) Installs /etc/systemd/system/skilldev-site.service
#   4) enable --now skilldev-site

set -euo pipefail

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/install-service.sh [SITE_ROOT]" >&2
  exit 1
fi

REPO_URL="https://github.com/Geeedy/site.git"
SITE_ROOT="${1:-/var/www/skilldev-site}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "[install] site root: $SITE_ROOT"

mkdir -p "$(dirname "$SITE_ROOT")"

if [[ -d "$SITE_ROOT/.git" ]]; then
  echo "[install] existing repo — fetch/reset to origin/main"
  git -C "$SITE_ROOT" remote set-url origin "$REPO_URL"
  git -C "$SITE_ROOT" fetch --prune origin main
  git -C "$SITE_ROOT" checkout main
  git -C "$SITE_ROOT" reset --hard origin/main
elif [[ "$SITE_ROOT" == "$SRC_REPO" ]]; then
  echo "[install] using current working tree as SITE_ROOT"
else
  echo "[install] cloning $REPO_URL → $SITE_ROOT"
  git clone --branch main "$REPO_URL" "$SITE_ROOT"
fi

chmod +x "$SITE_ROOT/deploy/"*.sh 2>/dev/null || true

if [[ ! -x "$SITE_ROOT/deploy/run-site.sh" ]]; then
  echo "[install] seeding deploy scripts from $SRC_REPO"
  mkdir -p "$SITE_ROOT/deploy" "$SITE_ROOT/tools"
  cp -a "$SRC_REPO/deploy/." "$SITE_ROOT/deploy/"
  cp -a "$SRC_REPO/tools/serve_i18n.py" "$SITE_ROOT/tools/" 2>/dev/null || true
  chmod +x "$SITE_ROOT/deploy/"*.sh
fi

if [[ ! -x "$SITE_ROOT/deploy/run-site.sh" ]]; then
  echo "ERROR: deploy/run-site.sh missing — push deploy/ to the repo first" >&2
  exit 1
fi

# Env file
ENV_FILE=/etc/skilldev-site.env
if [[ ! -f "$ENV_FILE" ]]; then
  sed "s|^SITE_ROOT=.*|SITE_ROOT=$SITE_ROOT|" "$SITE_ROOT/deploy/skilldev-site.env.example" > "$ENV_FILE"
  echo "[install] wrote $ENV_FILE"
else
  echo "[install] keep existing $ENV_FILE"
  # Append leads bot vars if missing
  if ! grep -q '^TELEGRAM_BOT_TOKEN=' "$ENV_FILE"; then
    {
      echo
      echo "# Leads Telegram bot — set TELEGRAM_BOT_TOKEN"
      echo "TELEGRAM_BOT_TOKEN="
      echo "LEADS_BOT_PASSWORD=skill-def-get-leads"
      echo "LEADS_DATA_DIR=/var/lib/skilldev"
    } >> "$ENV_FILE"
    echo "[install] appended leads bot env to $ENV_FILE"
  fi
fi

if grep -q '^TELEGRAM_BOT_TOKEN=$' "$ENV_FILE" || ! grep -q '^TELEGRAM_BOT_TOKEN=.\+' "$ENV_FILE"; then
  echo "[install] WARNING: set TELEGRAM_BOT_TOKEN in $ENV_FILE before leads bot can send messages" >&2
fi

mkdir -p /var/lib/skilldev
chmod 750 /var/lib/skilldev

# Unit file with correct WorkingDirectory / ExecStart
UNIT=/etc/systemd/system/skilldev-site.service
sed \
  -e "s|/var/www/skilldev-site|$SITE_ROOT|g" \
  "$SITE_ROOT/deploy/skilldev-site.service" > "$UNIT"
echo "[install] wrote $UNIT"

BOT_UNIT=/etc/systemd/system/skilldev-leads-bot.service
sed \
  -e "s|/var/www/skilldev-site|$SITE_ROOT|g" \
  "$SITE_ROOT/deploy/skilldev-leads-bot.service" > "$BOT_UNIT"
echo "[install] wrote $BOT_UNIT"

systemctl daemon-reload
systemctl enable skilldev-site.service skilldev-leads-bot.service
systemctl restart skilldev-site.service skilldev-leads-bot.service
systemctl --no-pager --full status skilldev-site.service || true
systemctl --no-pager --full status skilldev-leads-bot.service || true

echo
echo "[install] done. Useful commands:"
echo "  systemctl status skilldev-site"
echo "  systemctl status skilldev-leads-bot"
echo "  journalctl -u skilldev-site -f"
echo "  journalctl -u skilldev-leads-bot -f"
echo "  systemctl restart skilldev-site skilldev-leads-bot"
echo
echo "Telegram: open the bot → /start → password from LEADS_BOT_PASSWORD"
