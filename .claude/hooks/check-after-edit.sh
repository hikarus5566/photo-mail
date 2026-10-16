#!/bin/bash
# PostToolUse：改到 index.html 或 manifest.json 後自動跑檢查，失敗回傳 2 讓 Claude 看到錯誤並修正。
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  *index.html|*manifest.json) ;;
  *) exit 0 ;;
esac
cd "$CLAUDE_PROJECT_DIR" || exit 0
out=$(node scripts/check.mjs 2>&1) || { echo "$out" >&2; exit 2; }
