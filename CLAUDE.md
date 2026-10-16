# photo-mail

純靜態 PWA（照片寄信）：`index.html`（含全部 CSS/JS）＋ `manifest.json` ＋ 圖示。無 build、無套件管理。
外部依賴走 CDN：jsPDF、heic2any、Google Identity Services。

## 驗收指令
- `node scripts/check.mjs`：manifest 格式、內嵌 JS 語法、Playwright 開頁面無 console 錯誤。
- 改完一定要跑，並貼出指令與輸出當證據；失敗就繼續修，不要回報「完成」。

## 工作準則
- 動到 3 個以上檔案，或做法不確定：先寫計畫再改。
- 需求不清楚時，用選擇題（AskUserQuestion）問，包含我可能沒想到的邊界情況。
- 修根本原因，不要用 try/catch、跳過檢查或改測試來掩蓋錯誤。
- 大功能先把規格寫進 `SPEC.md`，再依規格實作。
- `index.html` 開頭的「設定」區塊放的是 Google OAuth 等設定值，不要隨意更動或刪除。

## 壓縮對話（/compact）時必須保留
- 已修改的檔案清單
- 驗收指令與最近一次結果
