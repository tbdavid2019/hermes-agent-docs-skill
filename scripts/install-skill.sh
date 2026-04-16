#!/bin/bash

set -euo pipefail

REPO_URL="${HERMES_AGENT_DOCS_SKILL_REPO_URL:-https://github.com/tbdavid2019/hermes-agent-docs-skill.git}"
DEFAULT_DEST="${HOME}/.codex/skills/hermes-agent-docs-skill"
DEST_DIR="${1:-$DEFAULT_DEST}"

echo "🦞 Hermes Agent docs skill installer"
echo "Destination: ${DEST_DIR}"

if [ -d "${DEST_DIR}/.git" ]; then
  echo "🔄 Existing git checkout detected. Updating..."
  git -C "${DEST_DIR}" pull --ff-only origin main
  echo "✅ Skill updated."
  exit 0
fi

if [ -e "${DEST_DIR}" ] && [ -n "$(find "${DEST_DIR}" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]; then
  echo "❌ ${DEST_DIR} already exists but is not a git checkout."
  echo "   Remove or rename that directory, then rerun this installer."
  echo "   This skill must be installed as a git checkout if you want updates to work."
  exit 1
fi

mkdir -p "$(dirname "${DEST_DIR}")"

if [ -d "${DEST_DIR}" ]; then
  rmdir "${DEST_DIR}" 2>/dev/null || true
fi

echo "📦 Cloning skill repository..."
git clone "${REPO_URL}" "${DEST_DIR}"
echo "✅ Skill installed."
echo "💡 Re-run this script later to update the installed checkout."
