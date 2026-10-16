# invest — 投資研究與提醒

僅供研究參考，不構成投資建議，不會自動下單。規格見 [SPEC.md](SPEC.md)、工具查證見 [VERIFY.md](VERIFY.md)。

## 提示詞範本（prompts/）
1. 把 `profile.md` 填好，貼到 Claude 專案的「專案指示」
2. 研究時用 `devils-advocate.md`、`earnings-check.md`、`weekly-review.md`

## Telegram 推播設定
1. Telegram 搜尋 **@BotFather** → `/newbot` → 取得 token
2. 對你的機器人傳任一訊息，再開 `https://api.telegram.org/bot<token>/getUpdates`，找 `"chat":{"id":...}` 的數字
3. GitHub repo → Settings → Secrets and variables → Actions → 新增
   `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`
4. 推到 main 後，Actions → invest-alert → Run workflow 手動測一次

## 本機執行
```
pip install -r invest/requirements.txt
python invest/notify.py --dry-run         # 真實資料，不推播
python invest/notify.py --fixture --dry-run  # 合成資料離線測試
```
追蹤標的改 `config.json`（台股加 `.TW`）。
