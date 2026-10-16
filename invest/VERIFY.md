# 影片工具查證（2026-10-16）

| 工具 | 存在？ | 重點 | 注意 |
|---|---|---|---|
| Yahoo Finance MCP | ✅ 多個開源實作（如 narumiruna/yfinance-mcp、maxscheijen/mcp-yahoo-finance） | 包裝 yfinance，免金鑰；台股代號加 `.TW` | 非官方 API，可能壞掉或被限流；選近期仍有維護的 |
| 金融業 Claude 外掛 | ✅ `anthropics/financial-services`（Anthropic 官方） | 法說會整理、同業比較、DCF 等；Claude Code：`claude plugin marketplace add anthropics/financial-services`；付費方案可用 | 輸出需人工檢查，不會下單 |
| TradingAgents | ✅ `TauricResearch/TradingAgents` | 分析師→多空辯論→風控→組合經理；支援 Anthropic 等模型 | 需另付 API 費；README 明寫僅供研究；論文績效有人質疑；星數各站說法不一（影片 11 萬未證實） |
| Daily Stock Analysis（影片的「daily stackeral／Dcker Adicing」） | ✅ `ZhuLinsen/daily_stock_analysis` | fork 後用 GitHub Actions 排程、推送 Telegram | 台股支援程度來源不一，以 README 為準；需另外的 AI 模型金鑰 |
| OpenBB / AI Hedge Fund | 未於本次查證 | — | 使用前看 README |

## 影片數字
外資賣超張數、0050 與台積電相關係數 0.92、回測勝率、股價區間等**皆未查證**，
其中相關係數與回檔回測可用本資料夾 `market.py` 自行重算。

## 結論
本資料夾的 B/C 不依賴上述任何專案，只用 yfinance＋Telegram，**不需 AI API 費用**。
想要「多空辯論」再自行評估 TradingAgents（另付費）。
