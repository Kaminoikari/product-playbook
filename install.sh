#!/usr/bin/env bash
# The Product Playbook — Install Script
# https://github.com/kaminoikari/product-playbook
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash
#   bash install.sh
#   bash install.sh --lang en
#   bash install.sh --lang zh-TW
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
COMMANDS_DIR="$HOME/.claude/commands"
SUPPORTED_LANGS="en zh-TW ja zh-CN es ko"
INSTALL_LANG=""

# ─── Language Detection ───────────────────────────────────────────────────────
detect_language() {
  # 1. Explicit env var
  if [ -n "${TPP_LANG:-}" ]; then
    echo "$TPP_LANG"
    return
  fi
  # 2. System locale
  local sys_lang="${LANG:-${LC_ALL:-${LC_MESSAGES:-}}}"
  case "$sys_lang" in
    zh_TW*|zh_Hant*) echo "zh-TW" ;;
    zh_CN*|zh_Hans*|zh*) echo "zh-CN" ;;
    ja*) echo "ja" ;;
    ko*) echo "ko" ;;
    es*) echo "es" ;;
    *)   echo "en" ;;
  esac
}

# ─── i18n Messages ────────────────────────────────────────────────────────────
msg() {
  local key="$1"
  case "$INSTALL_LANG" in
    zh-TW)
      case "$key" in
        title)              echo "The Product Playbook — 安裝程式" ;;
        usage_title)        echo "The Product Playbook — 安裝腳本" ;;
        usage_install)      echo "安裝或更新" ;;
        usage_lang)         echo "指定語言 (en, zh-TW)" ;;
        usage_uninstall)    echo "解除安裝" ;;
        usage_help)         echo "顯示此訊息" ;;
        usage_paths)        echo "安裝路徑：" ;;
        uninstalling)       echo "解除安裝 The Product Playbook..." ;;
        deleted_dir)        echo "已刪除" ;;
        dir_not_found)      echo "Skill 目錄不存在，跳過" ;;
        deleted_cmds)       echo "個 slash command 檔案已刪除" ;;
        no_cmds)            echo "未找到 product-*.md 指令檔案，跳過" ;;
        uninstall_done)     echo "解除安裝完成！" ;;
        git_not_found)      echo "找不到 git，請先安裝 git 後再執行。" ;;
        local_repo)         echo "偵測到本地 repo，使用本地檔案安裝..." ;;
        downloading)        echo "從 GitHub 下載最新版本..." ;;
        version)            echo "版本" ;;
        up_to_date)         echo "已是最新版本，無需更新。" ;;
        installed_at)       echo "已安裝：" ;;
        get_started)        echo "開始使用：" ;;
        start_claude)       echo "啟動 Claude Code，然後輸入：" ;;
        example_cmd)        echo "/product-quick 我想做一個記帳 App" ;;
        old_install)        echo "偵測到舊版安裝，更新中..." ;;
        installing_skill)   echo "安裝 Skill 檔案..." ;;
        skill_installed)    echo "Skill 已安裝至" ;;
        installing_cmds)    echo "安裝 Slash Commands..." ;;
        cmds_installed)     echo "個 slash commands 已安裝" ;;
        install_done)       echo "安裝完成！" ;;
        update_hint)        echo "更新：重新執行本安裝指令即可。" ;;
        uninstall_hint)     echo "解除安裝：" ;;
        unknown_arg)        echo "未知參數" ;;
        lang_label)         echo "語言" ;;
        invalid_lang)       echo "不支援的語言。支援：" ;;
      esac
      ;;
    *)
      case "$key" in
        title)              echo "The Product Playbook — Installer" ;;
        usage_title)        echo "The Product Playbook — Install Script" ;;
        usage_install)      echo "Install or update" ;;
        usage_lang)         echo "Set language (en, zh-TW)" ;;
        usage_uninstall)    echo "Uninstall" ;;
        usage_help)         echo "Show this message" ;;
        usage_paths)        echo "Install paths:" ;;
        uninstalling)       echo "Uninstalling The Product Playbook..." ;;
        deleted_dir)        echo "Deleted" ;;
        dir_not_found)      echo "Skill directory not found, skipping" ;;
        deleted_cmds)       echo "slash command file(s) deleted" ;;
        no_cmds)            echo "No product-*.md command files found, skipping" ;;
        uninstall_done)     echo "Uninstall complete!" ;;
        git_not_found)      echo "git not found. Please install git first." ;;
        local_repo)         echo "Local repo detected, installing from local files..." ;;
        downloading)        echo "Downloading latest version from GitHub..." ;;
        version)            echo "Version" ;;
        up_to_date)         echo "Already up to date, no update needed." ;;
        installed_at)       echo "Installed:" ;;
        get_started)        echo "Get started:" ;;
        start_claude)       echo "Launch Claude Code, then type:" ;;
        example_cmd)        echo "/product-quick I want to build an expense tracking app" ;;
        old_install)        echo "Previous installation detected, updating..." ;;
        installing_skill)   echo "Installing Skill files..." ;;
        skill_installed)    echo "Skill installed to" ;;
        installing_cmds)    echo "Installing Slash Commands..." ;;
        cmds_installed)     echo "slash commands installed" ;;
        install_done)       echo "Installation complete!" ;;
        update_hint)        echo "Update: re-run this install script." ;;
        uninstall_hint)     echo "Uninstall:" ;;
        unknown_arg)        echo "Unknown argument" ;;
        lang_label)         echo "Language" ;;
        invalid_lang)       echo "Unsupported language. Supported:" ;;
      esac
      ;;
  esac
}

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
${BOLD}$(msg usage_title)${RESET}

Usage:
  bash install.sh                  $(msg usage_install)
  bash install.sh --lang <lang>    $(msg usage_lang)
  bash install.sh --update         Update to latest version
  bash install.sh --uninstall      $(msg usage_uninstall)
  bash install.sh --help           $(msg usage_help)

$(msg usage_paths)
  Skill      → ~/.claude/skills/product-playbook/
  Commands   → ~/.claude/commands/product-*.md
EOF
}

# ─── Uninstall ────────────────────────────────────────────────────────────────
do_uninstall() {
  info "$(msg uninstalling)"

  if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    ok "$(msg deleted_dir) $SKILL_DIR"
  else
    warn "$(msg dir_not_found)"
  fi

  local count=0
  for f in "$COMMANDS_DIR"/product-*.md; do
    [ -f "$f" ] || continue
    rm -f "$f"
    count=$((count + 1))
  done

  if [ "$count" -gt 0 ]; then
    ok "$count $(msg deleted_cmds)"
  else
    warn "$(msg no_cmds)"
  fi

  printf "\n${GREEN}${BOLD}$(msg uninstall_done)${RESET}\n"
  exit 0
}

# ─── Install ──────────────────────────────────────────────────────────────────
do_install() {
  printf "\n${BOLD}🎯 $(msg title)${RESET}\n"
  printf "  $(msg lang_label): ${BOLD}$INSTALL_LANG${RESET}\n\n"

  # Check git
  if ! command -v git &>/dev/null; then
    err "$(msg git_not_found)"
    exit 1
  fi

  # Determine source: local repo or remote clone
  local src_dir=""
  local script_dir=""
  local commit_hash=""

  if [ -f "${BASH_SOURCE[0]:-}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi

  if [ -n "$script_dir" ] && [ -d "$script_dir/i18n" ]; then
    info "$(msg local_repo)"
    src_dir="$script_dir"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "")
    if [ -z "$commit_hash" ] && [ -f "$src_dir/package.json" ]; then
      commit_hash=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
    commit_hash="${commit_hash:-unknown}"
  elif [ -n "$script_dir" ] && [ -f "$script_dir/SKILL.md" ]; then
    # Fallback: legacy layout (no i18n directory)
    info "$(msg local_repo)"
    src_dir="$script_dir"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "")
    if [ -z "$commit_hash" ] && [ -f "$src_dir/package.json" ]; then
      commit_hash=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
    commit_hash="${commit_hash:-unknown}"
  else
    info "$(msg downloading)"
    git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null
    src_dir="$TMP_DIR"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local commit_date
    commit_date=$(git -C "$src_dir" log -1 --format='%ci' 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    ok "$(msg version): $commit_hash ($commit_date)"
  fi

  # Create directories
  mkdir -p "$SKILL_DIR" "$COMMANDS_DIR"

  # Get current package version (semver)
  local pkg_version=""
  if [ -f "$src_dir/package.json" ]; then
    pkg_version=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
  fi

  # Version check: skip if already up to date
  if [ -f "$SKILL_DIR/.version" ]; then
    local installed_version
    installed_version=$(cat "$SKILL_DIR/.version")
    # Detect legacy format (git hash, not semver) — force update
    if echo "$installed_version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
      # Semver format — compare with current package version
      if [ "$installed_version" = "$pkg_version" ] && [ -n "$pkg_version" ]; then
        ok "$(msg up_to_date) (v$pkg_version)"
        printf "\n$(msg installed_at)\n"
        printf "  Skill      → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
        printf "  Commands   → ${BOLD}%s${RESET}/product-*.md\n" "$COMMANDS_DIR"
        printf "\n$(msg get_started)\n"
        printf "  ${BOLD}claude${RESET} $(msg start_claude)\n"
        printf "  ${BLUE}$(msg example_cmd)${RESET}\n\n"
        return 0
      fi
    else
      # Legacy format (git hash or unknown) — always update
      warn "Detected legacy installation (v1.x). Upgrading to v${pkg_version:-latest}..."
    fi
  fi

  # Remove old installation
  if [ -d "$SKILL_DIR" ]; then
    info "$(msg old_install)"
    rm -rf "$SKILL_DIR"
    mkdir -p "$SKILL_DIR"
  fi

  # Determine default language source paths
  local default_lang_dir="$src_dir/i18n/$INSTALL_LANG"
  local has_i18n=false

  if [ -d "$src_dir/i18n" ]; then
    has_i18n=true
  fi

  # Copy Skill files
  info "$(msg installing_skill)"
  cp "$src_dir/LICENSE" "$SKILL_DIR/"

  if [ "$has_i18n" = true ]; then
    # Install ALL languages
    cp -r "$src_dir/i18n" "$SKILL_DIR/"
    ok "Installed all 6 languages to $SKILL_DIR/i18n/"

    # Set default language: copy SKILL.md, references/, commands/ from default lang
    if [ -d "$default_lang_dir" ]; then
      cp "$default_lang_dir/SKILL.md" "$SKILL_DIR/"
      cp -r "$default_lang_dir/references" "$SKILL_DIR/"
      cp -r "$default_lang_dir/commands" "$SKILL_DIR/"
    fi
  else
    # Legacy fallback: no i18n directory
    cp "$src_dir/SKILL.md" "$SKILL_DIR/"
    [ -d "$src_dir/references" ] && cp -r "$src_dir/references" "$SKILL_DIR/"
    [ -d "$src_dir/commands" ] && cp -r "$src_dir/commands" "$SKILL_DIR/"
  fi

  # Write version marker (semver from package.json for npm comparison)
  local pkg_version=""
  if [ -f "$src_dir/package.json" ]; then
    pkg_version=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
  fi
  if [ -n "$pkg_version" ]; then
    echo "$pkg_version" > "$SKILL_DIR/.version"
  elif [ "$commit_hash" != "unknown" ]; then
    echo "$commit_hash" > "$SKILL_DIR/.version"
  fi

  # Write default language marker
  echo "$INSTALL_LANG" > "$SKILL_DIR/.lang"

  ok "$(msg skill_installed) $SKILL_DIR"

  # Copy slash commands to global commands dir
  info "$(msg installing_cmds)"
  local cmds_src="$SKILL_DIR/commands"
  local cmd_count=0
  for f in "$cmds_src"/*.md; do
    [ -f "$f" ] || continue
    cp "$f" "$COMMANDS_DIR/"
    cmd_count=$((cmd_count + 1))
  done
  ok "$cmd_count $(msg cmds_installed)"

  # Done
  printf "\n${GREEN}${BOLD}$(msg install_done)${RESET}\n\n"
  printf "$(msg installed_at)\n"
  printf "  Skill      → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
  printf "  Commands   → ${BOLD}%s${RESET}/product-*.md\n" "$COMMANDS_DIR"
  printf "\n$(msg get_started)\n"
  printf "  ${BOLD}claude${RESET} $(msg start_claude)\n"
  printf "  ${BLUE}$(msg example_cmd)${RESET}\n"
  printf "\n$(msg update_hint)\n"
  printf "$(msg uninstall_hint) ${YELLOW}bash install.sh --uninstall${RESET}\n\n"
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
  # Parse --lang argument first
  local args=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --lang)
        if [ -n "${2:-}" ]; then
          INSTALL_LANG="$2"
          shift 2
        else
          err "$(msg invalid_lang) $SUPPORTED_LANGS"
          exit 1
        fi
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done

  # Auto-detect default language if not specified
  if [ -z "$INSTALL_LANG" ]; then
    INSTALL_LANG=$(detect_language)
  fi

  # Validate language (fallback to en if unsupported)
  local valid=false
  for lang in $SUPPORTED_LANGS; do
    if [ "$INSTALL_LANG" = "$lang" ]; then
      valid=true
      break
    fi
  done
  if [ "$valid" = false ]; then
    warn "'$INSTALL_LANG' is not supported. Supported: $SUPPORTED_LANGS"
    warn "Falling back to English (en)."
    INSTALL_LANG="en"
  fi

  # Dispatch command
  case "${args[0]:-}" in
    --uninstall|-u)
      do_uninstall
      ;;
    --update)
      # Update: detect installed language, then re-install from remote
      if [ -f "$SKILL_DIR/.lang" ]; then
        INSTALL_LANG=$(cat "$SKILL_DIR/.lang")
      fi
      # Force re-download by removing version file
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
      err "$(msg unknown_arg): ${args[0]}"
      usage
      exit 1
      ;;
  esac
}

main "$@"
