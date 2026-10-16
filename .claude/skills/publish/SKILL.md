---
name: publish
description: 檢查通過後把目前變更發布到 main（GitHub Pages 上線）。
disable-model-invocation: true
---

依序執行，任何一步失敗就停下並回報，不要跳過：

1. `git status` 確認有要發布的變更；沒有就停止。
2. 執行 `node scripts/check.mjs`，貼出完整輸出。失敗就停止，不要發布。
3. 列出 `git diff --stat` 並用一句話說明變更內容，等使用者確認。
4. 確認後 commit（訊息描述變更），再 `git push origin HEAD:main`。
5. 回報 push 結果與 commit hash。
