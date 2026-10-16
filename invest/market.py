"""市場溫度計與回檔門檻計算。僅供研究，不構成投資建議。"""
import math
import zlib

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def fetch(tickers, fixture=False):
    """回傳 {ticker: 收盤價 Series}，約兩年資料。"""
    if fixture:
        return {t: _synthetic(t) for t in tickers}
    import yfinance as yf
    out = {}
    for t in tickers:
        s = yf.Ticker(t).history(period="2y", auto_adjust=True)["Close"].dropna()
        if len(s) >= 200:
            out[t] = s
        else:
            print(f"[warn] {t} 資料不足（{len(s)} 筆），略過")
    return out


def _synthetic(ticker, n=500):
    rng = np.random.default_rng(zlib.crc32(ticker.encode()))
    vol = 0.03 if ticker in ("NVDA", "^VIX") else 0.015
    rets = rng.normal(0.0004, vol, n)
    idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n)
    return pd.Series(100 * np.exp(np.cumsum(rets)), index=idx)


def stats(s):
    last = s.iloc[-1]
    daily_vol = s.pct_change().dropna().iloc[-TRADING_DAYS:].std()
    monthly_vol = daily_vol * math.sqrt(21)
    return {
        "price": last,
        "vs_ma200": last / s.iloc[-200:].mean() - 1,
        "vs_high52": last / s.iloc[-TRADING_DAYS:].max() - 1,
        "vs_high20": last / s.iloc[-20:].max() - 1,
        "ann_vol": daily_vol * math.sqrt(TRADING_DAYS),
        "tiers": (max(0.05, monthly_vol), max(0.10, 2 * monthly_vol)),
    }


def backtest(s, threshold, horizon=60, gap=60):
    """首次跌破「離 52 週高點 -threshold」後 horizon 日報酬。"""
    dd = s / s.rolling(TRADING_DAYS, min_periods=60).max() - 1
    rets, last_i = [], -gap
    for i in range(len(s) - horizon):
        if dd.iloc[i] <= -threshold and i - last_i >= gap:
            rets.append(s.iloc[i + horizon] / s.iloc[i] - 1)
            last_i = i
    if not rets:
        return {"n": 0}
    return {"n": len(rets), "win": sum(r > 0 for r in rets) / len(rets), "worst": min(rets)}


def temperature(watch_stats, vix=None):
    avg = sum(st["vs_ma200"] for st in watch_stats.values()) / len(watch_stats)
    label = "偏熱" if avg > 0.15 else "偏冷" if avg < -0.05 else "中性"
    if vix is not None and vix > 25:
        label += "（VIX 恐慌）"
    return label, avg
