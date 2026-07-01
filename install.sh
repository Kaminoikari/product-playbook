#!/usr/bin/env bash
# The Product Playbook — Install Script
# https://github.com/kaminoikari/product-playbook
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash
#   bash install.sh
#   bash install.sh --update
#   bash install.sh --uninstall
#   bash install.sh --help

set -euo pipefail

# ─── Colors ───────────────────────────────────────────────────────────────────
if [ -z "${NO_COLOR:-}" ] && [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' BOLD='' RESET=''
fi

# ─── Constants ────────────────────────────────────────────────────────────────
REPO_URL="https://github.com/kaminoikari/product-playbook.git"
TMP_DIR="${TMPDIR:-/tmp}/product-playbook-install-$$"
SKILL_DIR="$HOME/.claude/skills/product-playbook"

# Top-level entries that make up the shippable plugin. Dev artifacts
# (.git, node_modules, docs, logs, tests, evals, scripts, .superpowers)
# are intentionally excluded — this installs the plugin, not the repo.
SHIP_ENTRIES=(".claude-plugin" "skills" "hooks" "agents" "references" "LICENSE" "README.md" "package.json")

# ─── Helpers ──────────────────────────────────────────────────────────────────
info()  { printf "${BLUE}▸${RESET} %s\n" "$*"; }
ok()    { printf "${GREEN}✓${RESET} %s\n" "$*"; }
warn()  { printf "${YELLOW}⚠${RESET} %s\n" "$*"; }
err()   { printf "${RED}✗${RESET} %s\n" "$*" >&2; }

cleanup() {
  if [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

usage() {
  cat <<EOF
${BOLD}The Product Playbook — Install Script${RESET}

Usage:
  bash install.sh                  Install or update
  bash install.sh --update         Update to latest version
  bash install.sh --uninstall      Uninstall
  bash install.sh --help           Show this message

Install path:
  Skill/plugin → ~/.claude/skills/product-playbook/
EOF
}

# ─── Uninstall ────────────────────────────────────────────────────────────────
do_uninstall() {
  info "Uninstalling The Product Playbook..."

  if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    ok "Deleted $SKILL_DIR"
  else
    warn "Skill directory not found, skipping"
  fi

  printf "\n${GREEN}${BOLD}Uninstall complete!${RESET}\n"
  exit 0
}

# ─── Install ──────────────────────────────────────────────────────────────────
do_install() {
  printf "\n${BOLD}🎯 The Product Playbook — Installer${RESET}\n\n"

  # Check git
  if ! command -v git &>/dev/null; then
    err "git not found. Please install git first."
    exit 1
  fi

  # Determine source: local repo or remote clone
  local src_dir=""
  local script_dir=""
  local commit_hash=""

  if [ -f "${BASH_SOURCE[0]:-}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi

  if [ -n "$script_dir" ] && [ -f "$script_dir/.claude-plugin/plugin.json" ]; then
    info "Local repo detected, installing from local files..."
    src_dir="$script_dir"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "")
    if [ -z "$commit_hash" ] && [ -f "$src_dir/package.json" ]; then
      commit_hash=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
    commit_hash="${commit_hash:-unknown}"
  else
    info "Downloading latest version from GitHub..."
    git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null
    src_dir="$TMP_DIR"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local commit_date
    commit_date=$(git -C "$src_dir" log -1 --format='%ci' 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    ok "Version: $commit_hash ($commit_date)"
  fi

  # Get current package version (semver)
  local pkg_version=""
  if [ -f "$src_dir/package.json" ]; then
    pkg_version=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
  fi

  # Version check: skip if already up to date
  if [ -f "$SKILL_DIR/.version" ]; then
    local installed_version
    installed_version=$(cat "$SKILL_DIR/.version")
    if [ "$installed_version" = "$pkg_version" ] && [ -n "$pkg_version" ]; then
      ok "Already up to date, no update needed. (v$pkg_version)"
      printf "\nInstalled:\n"
      printf "  Skill/plugin → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
      printf "\nGet started:\n"
      printf "  Run ${BOLD}/reload-plugins${RESET} in Claude Code (or restart it), then try ${BLUE}/product-playbook${RESET}.\n\n"
      return 0
    fi
  fi

  # Remove old installation, then copy in the allowlisted entries
  info "Installing plugin files..."
  rm -rf "$SKILL_DIR"
  mkdir -p "$SKILL_DIR"

  for entry in "${SHIP_ENTRIES[@]}"; do
    if [ -e "$src_dir/$entry" ]; then
      cp -R "$src_dir/$entry" "$SKILL_DIR/"
    fi
  done

  # Write version marker (semver from package.json for update comparison)
  if [ -n "$pkg_version" ]; then
    echo "$pkg_version" > "$SKILL_DIR/.version"
  elif [ "$commit_hash" != "unknown" ]; then
    echo "$commit_hash" > "$SKILL_DIR/.version"
  fi

  ok "Installed to $SKILL_DIR"

  # Done
  printf "\n${GREEN}${BOLD}Installation complete!${RESET}\n\n"
  printf "Installed:\n"
  printf "  Skill/plugin → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
  printf "\nRun ${BOLD}/reload-plugins${RESET} in Claude Code (or restart it), then try:\n"
  printf "  ${BLUE}/product-playbook${RESET} I want to build an expense tracking app\n"
  printf "\nUpdate: re-run this install script, or ${BOLD}bash install.sh --update${RESET}.\n"
  printf "Uninstall: ${YELLOW}bash install.sh --uninstall${RESET}\n\n"
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
  case "${1:-}" in
    --uninstall|-u)
      do_uninstall
      ;;
    --update)
      # Force re-install by removing the version marker first.
      rm -f "$SKILL_DIR/.version"
      do_install
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    "")
      do_install
      ;;
    *)
      err "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
}

main "$@"
