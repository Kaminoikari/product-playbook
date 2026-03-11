#!/usr/bin/env bash
# The Product Playbook — 一鍵安裝腳本
# https://github.com/kaminoikari/the-product-playbook
#
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash
#   bash install.sh
#   bash install.sh --uninstall
#   bash install.sh --help

set -euo pipefail

# ─── 色彩設定 ───────────────────────────────────────────────────────────────────
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

# ─── 常數 ─────────────────────────────────────────────────────────────────────
REPO_URL="https://github.com/kaminoikari/the-product-playbook.git"
TMP_DIR="${TMPDIR:-/tmp}/the-product-playbook-install-$$"
SKILL_DIR="$HOME/.claude/skills/the-product-playbook"
COMMANDS_DIR="$HOME/.claude/commands"

# ─── 輔助函式 ──────────────────────────────────────────────────────────────────
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
${BOLD}The Product Playbook — 安裝腳本${RESET}

用法：
  bash install.sh              安裝或更新
  bash install.sh --uninstall  解除安裝
  bash install.sh --help       顯示此訊息

安裝路徑：
  Skill      → ~/.claude/skills/the-product-playbook/
  Commands   → ~/.claude/commands/product-*.md
EOF
}

# ─── 解除安裝 ──────────────────────────────────────────────────────────────────
do_uninstall() {
  info "解除安裝 The Product Playbook..."

  if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    ok "已刪除 $SKILL_DIR"
  else
    warn "Skill 目錄不存在，跳過"
  fi

  local count=0
  for f in "$COMMANDS_DIR"/product-*.md; do
    [ -f "$f" ] || continue
    rm -f "$f"
    count=$((count + 1))
  done

  if [ "$count" -gt 0 ]; then
    ok "已刪除 $count 個 slash command 檔案"
  else
    warn "未找到 product-*.md 指令檔案，跳過"
  fi

  printf "\n${GREEN}${BOLD}解除安裝完成！${RESET}\n"
  exit 0
}

# ─── 安裝 ──────────────────────────────────────────────────────────────────────
do_install() {
  printf "\n${BOLD}🎯 The Product Playbook — 安裝程式${RESET}\n\n"

  # 檢查 git
  if ! command -v git &>/dev/null; then
    err "找不到 git，請先安裝 git 後再執行。"
    exit 1
  fi

  # 判斷來源：本地 repo 或遠端 clone
  local src_dir=""
  local script_dir=""
  local commit_hash=""

  # 取得腳本所在目錄（如果是檔案執行而非 pipe）
  if [ -f "${BASH_SOURCE[0]:-}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi

  # 如果腳本在 repo 目錄內（有 SKILL.md），直接用本地檔案
  if [ -n "$script_dir" ] && [ -f "$script_dir/SKILL.md" ]; then
    info "偵測到本地 repo，使用本地檔案安裝..."
    src_dir="$script_dir"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "")
    # 無 git 時（npx 安裝），使用 package.json version
    if [ -z "$commit_hash" ] && [ -f "$src_dir/package.json" ]; then
      commit_hash=$(grep '"version"' "$src_dir/package.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
    commit_hash="${commit_hash:-unknown}"
  else
    info "從 GitHub 下載最新版本..."
    git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null
    src_dir="$TMP_DIR"
    commit_hash=$(git -C "$src_dir" rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local commit_date
    commit_date=$(git -C "$src_dir" log -1 --format='%ci' 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    ok "版本：$commit_hash ($commit_date)"
  fi

  # 建立目錄
  mkdir -p "$SKILL_DIR" "$COMMANDS_DIR"

  # 版本比對：已是最新版本則跳過安裝
  if [ -f "$SKILL_DIR/.version" ]; then
    local installed_version
    installed_version=$(cat "$SKILL_DIR/.version")
    if [ "$installed_version" = "$commit_hash" ] && [ "$commit_hash" != "unknown" ]; then
      ok "已是最新版本 ($commit_hash)，無需更新。"
      printf "\n已安裝：\n"
      printf "  Skill      → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
      printf "  Commands   → ${BOLD}%s${RESET}/product-*.md\n" "$COMMANDS_DIR"
      printf "\n開始使用：\n"
      printf "  ${BOLD}claude${RESET} 啟動 Claude Code，然後輸入：\n"
      printf "  ${BLUE}/product-quick 我想做一個記帳 App${RESET}\n\n"
      return 0
    fi
  fi

  # 清除舊安裝
  if [ -d "$SKILL_DIR" ]; then
    info "偵測到舊版安裝，更新中..."
    rm -rf "$SKILL_DIR"
    mkdir -p "$SKILL_DIR"
  fi

  # 複製 Skill 檔案
  info "安裝 Skill 檔案..."
  cp "$src_dir/SKILL.md" "$SKILL_DIR/"
  cp "$src_dir/LICENSE" "$SKILL_DIR/"
  cp "$src_dir/README.md" "$SKILL_DIR/"

  if [ -d "$src_dir/references" ]; then
    cp -r "$src_dir/references" "$SKILL_DIR/"
  fi

  if [ -d "$src_dir/commands" ]; then
    cp -r "$src_dir/commands" "$SKILL_DIR/"
  fi

  # 寫入版本標記
  if [ "$commit_hash" != "unknown" ]; then
    echo "$commit_hash" > "$SKILL_DIR/.version"
  fi

  ok "Skill 已安裝至 $SKILL_DIR"

  # 複製 slash commands
  info "安裝 Slash Commands..."
  local cmd_count=0
  for f in "$src_dir"/commands/*.md; do
    [ -f "$f" ] || continue
    cp "$f" "$COMMANDS_DIR/"
    cmd_count=$((cmd_count + 1))
  done
  ok "已安裝 $cmd_count 個 slash commands"

  # 完成
  printf "\n${GREEN}${BOLD}安裝完成！${RESET}\n\n"
  printf "已安裝：\n"
  printf "  Skill      → ${BOLD}%s${RESET}\n" "$SKILL_DIR"
  printf "  Commands   → ${BOLD}%s${RESET}/product-*.md\n" "$COMMANDS_DIR"
  printf "\n開始使用：\n"
  printf "  ${BOLD}claude${RESET} 啟動 Claude Code，然後輸入：\n"
  printf "  ${BLUE}/product-quick 我想做一個記帳 App${RESET}\n"
  printf "\n更新：重新執行本安裝指令即可。\n"
  printf "解除安裝：${YELLOW}bash install.sh --uninstall${RESET}\n\n"
}

# ─── 主程式 ────────────────────────────────────────────────────────────────────
main() {
  case "${1:-}" in
    --uninstall|-u)
      do_uninstall
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    "")
      do_install
      ;;
    *)
      err "未知參數：$1"
      usage
      exit 1
      ;;
  esac
}

main "$@"
