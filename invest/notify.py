"""產生市場報告，觸發回檔門檻時推播 Telegram。僅供研究，不構成投資建議。"""
import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

import market

HERE = Path(__file__).parent
STATE = HERE / "state.json"


def pct(x):
    return f"{x * 100:+.1f}%"


def build(fixture):
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    watch, ind = cfg["watchlist"], cfg["indicators"]
    data = market.fetch(list(watch) + list(ind), fixture)
    ws = {t: market.stats(data[t]) for t in watch if t in data}
    vix = data["^VIX"].iloc[-1] if "^VIX" in data else None
    label, avg = market.temperature(ws, vix)

    lines = [f"📊 市場溫度：{label}（自選平均離 200MA {pct(avg)}）", "", "【指標】"]
    for t, name in ind.items():
        if t in data:
            st = market.stats(data[t])
            lines.append(f"{name} {st['price']:.2f}｜200MA {pct(st['vs_ma200'])}｜52週高 {pct(st['vs_high52'])}")

    alerts = []
    lines += ["", "【自選】"]
    for t, st in ws.items():
        t1, t2 = st["tiers"]
        bt = market.backtest(data[t], t1)
        bt_txt = f"回測 {bt['n']} 次 勝率 {bt['win']:.0%} 最差 {pct(bt['worst'])}" if bt["n"] else "回測無樣本"
        lines.append(
            f"{watch[t]}（{t}）{st['price']:.2f}｜200MA {pct(st['vs_ma200'])}｜52週高 {pct(st['vs_high52'])}"
            f"｜門檻 -{t1:.0%}/-{t2:.0%}｜{bt_txt}"
        )
        level = 2 if st["vs_high52"] <= -t2 else 1 if st["vs_high52"] <= -t1 else 0
        if level:
            alerts.append((f"{t}:L{level}", f"⚠️ {watch[t]} 離 52 週高點 {pct(st['vs_high52'])}，達第 {level} 級門檻"))
    lines += ["", "※ 僅供研究參考，不構成投資建議。"]
    return "\n".join(lines), alerts, cfg["cooldown_hours"]


def fresh_alerts(alerts, cooldown_h):
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    now = time.time()
    new = [msg for key, msg in alerts if now - state.get(key, 0) > cooldown_h * 3600]
    for key, msg in alerts:
        if msg in new:
            state[key] = now
    STATE.write_text(json.dumps(state))
    return new


def send(text):
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        print("[info] 未設定 TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID，不推播")
        return
    body = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", body, timeout=20)
    print("[info] 已推播 Telegram")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", action="store_true", help="用合成資料離線測試")
    ap.add_argument("--dry-run", action="store_true", help="不送出 Telegram")
    ap.add_argument("--always", action="store_true", help="沒觸發也推送完整報告")
    a = ap.parse_args()

    report, alerts, cooldown = build(a.fixture)
    print(report)
    new = fresh_alerts(alerts, cooldown) if not a.dry_run else [m for _, m in alerts]
    print("\n".join(["", "【本次提醒】"] + (new or ["（無）"])))
    if a.dry_run:
        return
    if new or a.always:
        send("\n".join(new + ["", report]))


if __name__ == "__main__":
    main()
