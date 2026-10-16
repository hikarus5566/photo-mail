# invest/ 規格

研究與提醒工具，**不構成投資建議，不自動下單**。

## A. 提示詞範本（`prompts/`）
- `profile.md`：投資人檔案範本（目標、期限、可承受虧損、禁止清單、推翻條件）。
- `devils-advocate.md`：「不要給建議，專挑我毛病」＋推翻條件。
- `earnings-check.md`：法說會整理，每個數字附來源，查不到寫「查不到」。
- `weekly-review.md`：每週檢討＋選股是否贏過大盤 ETF。

## B. 市場溫度計＋回檔提醒（`market.py`）
- 標的：`config.json` 的 `watchlist`；指標：`indicators`（大盤、費半、VIX、10 年期殖利率）。
- 每檔計算：最新價、離 200 日均線 %、離 52 週高點 %、離 20 日高點 %、年化波動率。
- 溫度：自選標的離 200MA 平均 > +15% 偏熱、< -5% 偏冷、其餘中性；VIX > 25 加註恐慌。
- 回檔門檻依波動自動設定：月波動 σm = 日波動 × √21；
  第 1 級 = max(5%, 1σm)，第 2 級 = max(10%, 2σm)，以「離 52 週高點」判斷。
- 回測：過去資料中首次跌破門檻（距上次觸發至少 60 交易日）後 60 日報酬，列出次數、勝率、最差。

## C. Telegram 推播（`notify.py` ＋ `.github/workflows/invest.yml`）
- 排程：平日台股 08:30、14:00，美股 21:00、05:30（台灣時間），另可手動觸發。
- 有觸發門檻才推播；同標的同級提醒 72 小時內不重發（`state.json`，以 Actions cache 保存）。
- Secrets：`TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`；未設定時只印出不推播。
- `--fixture`：用合成資料離線測試；`--dry-run`：不送出。

## D. 查證（`VERIFY.md`）
影片提到的工具是否存在、用途、費用、注意事項。

## 驗收
- `python3 invest/notify.py --fixture --dry-run` 正常輸出報告。
- `node scripts/check.mjs` 通過（確認未影響 photo-mail）。
