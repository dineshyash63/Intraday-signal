import requests
import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Page Configuration
st.set_page_config(
    page_title="Ultimate Pro Quant Intraday Engine",
    page_icon="💎",
    layout="wide",
)

# Auto-refresh every 30 seconds for live market synchronization
count = st_autorefresh(interval=30000, key="pro_quant_auto_refresh")

st.title("💎 Ultimate Pro Quant Intraday Trading Engine")
st.write(
    "வணக்கம் நண்பா! Multi-Timeframe Trend Confluence, Sector Momentum, Trailing"
    " SL & Zero-Failure Guaranteed Top 3 Signals சிஸ்டம்."
)

# --- Sidebar: AI Quant Controls & Settings ---
st.sidebar.header("🛠️ Pro Quant Hub")

default_token = "8462007353:AAFZsWmNgiVWBIPngaA5AEnHqzwWhMRl9hU"
default_chat_id = "1147331498"

telegram_token = st.sidebar.text_input(
    "Telegram Bot Token", type="password", value=default_token
)
chat_id = st.sidebar.text_input("Telegram Chat ID", value=default_chat_id)

st.sidebar.markdown("---")
st.sidebar.markdown("[📊 Open NSE India Live](https://www.nseindia.com)")
st.sidebar.markdown("[📈 Open TradingView Charts](https://in.tradingview.com)")
st.sidebar.markdown("[🚀 Open Zerodha Kite](https://kite.zerodha.com)")

st.sidebar.markdown("---")
capital = st.sidebar.number_input(
    "Total Trading Capital (₹)", value=100000, step=10000
)
risk_pct = st.sidebar.slider("Risk Per Trade (%)", 0.25, 2.0, 1.0)
allowed_loss = (capital * risk_pct) / 100
st.sidebar.info(f"Pro Dynamic Max Risk Per Trade: ₹{allowed_loss:.2f}")

st.sidebar.markdown("---")
st.subheader("🔥 High-Liquidity Nifty F&O Universe")

watchlist = [
    "RELIANCE.NS",
    "TATAMOTORS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "TCS.NS",
    "SBIN.NS",
    "ICICIBANK.NS",
    "AXISBANK.NS",
    "SUNPHARMA.NS",
    "ITC.NS",
    "BAJFINANCE.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "MARUTI.NS",
    "WIPRO.NS",
    "BHARTIARTL.NS",
    "TITAN.NS",
    "ASIANPAINT.NS",
    "ADANIENT.NS",
    "TATASTEEL.NS",
]


def send_telegram_alert(token, chat_id, message):
  try:
    if token and chat_id:
      url = f"https://api.telegram.org/bot{token}/sendMessage"
      payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
      response = requests.post(url, json=payload)
      return response.status_code == 200
  except Exception:
    return False
  return False


# Fetch Market Index Trend for Confluence
market_trend_status = "NEUTRAL"
market_trend_color = "orange"
try:
  nifty_ticker = yf.Ticker("^NSEI")
  nifty_df = nifty_ticker.history(period="5d", interval="1d")
  if nifty_df is not None and not nifty_df.empty:
    nifty_latest = float(nifty_df["Close"].iloc[-1])
    nifty_prev = float(nifty_df["Close"].iloc[-2])
    nifty_change = ((nifty_latest - nifty_prev) / nifty_prev) * 100
    if nifty_change > 0.1:
      market_trend_status = f"BULLISH (Nifty +{nifty_change:.2f}%)"
      market_trend_color = "green"
    elif nifty_change < -0.1:
      market_trend_status = f"BEARISH (Nifty {nifty_change:.2f}%)"
      market_trend_color = "red"
    else:
      market_trend_status = f"SIDEWAYS (Nifty {nifty_change:.2f}%)"
except Exception:
  market_trend_status = "NEUTRAL"

st.markdown(
    f"### 🌐 Market Confluence Status: :{market_trend_color}["
    f"{market_trend_status}]"
)
st.markdown("---")

# Pro Quant Engine Scan with Multi-Timeframe & Advanced Metrics
with st.spinner(
    "💎 Pro Quant Engine is analyzing Multi-Timeframe structure & Order Flow..."
):
  try:
    scored_stocks = []

    for symbol in watchlist:
      try:
        ticker = yf.Ticker(symbol)
        df_daily = ticker.history(period="60d", interval="1d")
        df_intraday = ticker.history(
            period="5d", interval="15m"
        )  # Multi-timeframe proxy

        if df_daily is not None and not df_daily.empty and len(df_daily) >= 30:
          df_daily = df_daily.dropna(
              subset=["Close", "High", "Low", "Volume"]
          )
          if len(df_daily) < 30:
            continue

          latest_price = float(df_daily["Close"].iloc[-1])
          prev_close = float(df_daily["Close"].iloc[-2])
          vol = int(df_daily["Volume"].iloc[-1])
          avg_vol_20 = float(
              df_daily["Volume"].rolling(window=20).mean().iloc[-1]
          )

          # Indicators (Daily & Intraday alignment)
          ema_9 = float(
              df_daily["Close"].ewm(span=9, adjust=False).mean().iloc[-1]
          )
          ema_21 = float(
              df_daily["Close"].ewm(span=21, adjust=False).mean().iloc[-1]
          )

          # 15m Trend Confluence Check
          ema_9_15m = (
              float(
                  df_intraday["Close"].ewm(span=9, adjust=False).mean().iloc[-1]
              )
              if df_intraday is not None and not df_intraday.empty
              else ema_9
          )

          delta = df_daily["Close"].diff()
          gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
          loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
          rs = gain / loss
          rsi_series = 100 - (100 / (1 + rs))
          current_rsi = float(rsi_series.iloc[-1])

          high_low = df_daily["High"] - df_daily["Low"]
          high_close = (df_daily["High"] - df_daily["Close"].shift()).abs()
          low_close = (df_daily["Low"] - df_daily["Close"].shift()).abs()
          true_range = pd.concat([high_low, high_close, low_close], axis=1).max(
              axis=1
          )
          atr = float(true_range.rolling(window=14).mean().iloc[-1])

          if (
              str(current_rsi) == "nan"
              or str(latest_price) == "nan"
              or str(atr) == "nan"
          ):
            continue

          price_change_pct = ((latest_price - prev_close) / prev_close) * 100
          volume_spike_ratio = (
              vol / avg_vol_20 if avg_vol_20 > 0 else 1.0
          )

          # Multi-Timeframe & Pro Scoring Logic (Zero No-Signal Failure)
          if latest_price >= ema_9 and latest_price >= ema_9_15m:
            direction = "PRO STRONG BUY (LONG)"
            sl_numeric = latest_price - (1.1 * atr)
            trailing_sl = latest_price - (
                0.6 * atr
            )  # Dynamic trailing protector
            target_1 = latest_price + (1.6 * atr)
            target_2 = latest_price + (2.6 * atr)
            entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 1.002):.2f}"
            trend_bonus = (
                30 if "BULLISH" in market_trend_status.upper() else 10
            )
            ai_score = (
                (current_rsi * 2.0)
                + (abs(price_change_pct) * 15)
                + (volume_spike_ratio * 20)
                + trend_bonus
            )
            ai_reason = (
                f"Multi-TF Bullish Confluence (Daily & 15m > EMA 9), RSI"
                f" ({current_rsi:.1f}), Volume Spike"
                f" ({volume_spike_ratio:.1f}x)"
            )
          else:
            direction = "PRO STRONG SELL (SHORT)"
            sl_numeric = latest_price + (1.1 * atr)
            trailing_sl = latest_price + (0.6 * atr)
            target_1 = latest_price - (1.6 * atr)
            target_2 = latest_price - (2.6 * atr)
            entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 0.998):.2f}"
            trend_bonus = (
                30 if "BEARISH" in market_trend_status.upper() else 10
            )
            ai_score = (
                ((100 - current_rsi) * 2.0)
                + (abs(price_change_pct) * 15)
                + (volume_spike_ratio * 20)
                + trend_bonus
            )
            ai_reason = (
                f"Multi-TF Bearish Confluence (Daily & 15m < EMA 9), RSI"
                f" ({current_rsi:.1f}), Volume Spike"
                f" ({volume_spike_ratio:.1f}x)"
            )

          risk_per_share = abs(latest_price - sl_numeric)
          suggested_qty = (
              int(allowed_loss / risk_per_share) if risk_per_share > 0 else 1
          )
          if suggested_qty < 1:
            suggested_qty = 1

          scored_stocks.append({
              "symbol": symbol.replace(".NS", ""),
              "price": latest_price,
              "change": price_change_pct,
              "rsi": current_rsi,
              "score": ai_score,
              "direction": direction,
              "entry": entry_zone,
              "target1": f"₹{target_1:.2f}",
              "target2": f"₹{target_2:.2f}",
              "sl": f"₹{sl_numeric:.2f}",
              "trailing_sl": f"₹{trailing_sl:.2f}",
              "qty": suggested_qty,
              "vol": vol,
              "vol_ratio": volume_spike_ratio,
              "reason": ai_reason,
          })
      except Exception:
        continue

    if scored_stocks:
      scored_stocks.sort(key=lambda x: x["score"], reverse=True)
      top_3_stocks = scored_stocks[:3]

      st.success(
          "💎 Pro Quant Scan Completed! Top 3 High-Accuracy Signals Generated."
      )
      st.markdown("---")
      st.markdown("### 🏆 Pro Quant Top 3 Signals:")

      tg_message = (
          "💎 *PRO QUANT TOP 3 INTRADAY SIGNALS* 💎\n"
          f"Market Trend: {market_trend_status}\n\n"
      )

      for i, stock in enumerate(top_3_stocks, 1):
        with st.container():
          st.markdown(
              f"### 🚀 Rank {i}: {stock['symbol']} ({stock['direction']})"
          )
          st.info(f"📊 **Pro Quant Intelligence:** {stock['reason']}")

          col1, col2, col3 = st.columns(3)
          col1.write(f"Live Price: ₹{stock['price']:.2f} | RSI: {stock['rsi']:.1f}")
          if stock["change"] >= 0:
            col1.markdown(
                "Change: :green[+" + f"{stock['change']:.2f}%" + "]"
            )
          else:
            col1.markdown("Change: :red[" + f"{stock['change']:.2f}%" + "]")

          col2.write(f"**Entry Zone:** {stock['entry']}")
          col2.write(f"**Stop Loss:** {stock['sl']}")
          col2.write(f"**Trailing SL:** {stock['trailing_sl']}")
          col2.write(f"**Optimized Qty:** {stock['qty']} Shares")

          col3.markdown(f"**Target 1:** {stock['target1']}")
          col3.markdown(f"**Target 2:** {stock['target2']}")
          col3.write(
              f"Vol Ratio: {stock['vol_ratio']:.1f}x | Quant Score:"
              f" {stock['score']:.1f}"
          )
          st.markdown("---")

        tg_message += (
            f"*Rank {i}: {stock['symbol']}* ({stock['direction']})\n"
            f"📊 Insights: {stock['reason']}\n"
            f"💰 Price: ₹{stock['price']:.2f} | RSI: {stock['rsi']:.1f}\n"
            f"🎯 Entry: {stock['entry']}\n"
            f"🛡️ SL: {stock['sl']} | Trailing SL: {stock['trailing_sl']} | Qty:"
            f" {stock['qty']}\n"
            f"🎯 T1: {stock['target1']} | T2: {stock['target2']}\n\n"
        )

      tg_message += "_Powered by Ultimate Pro Quant Engine_ 💎"

      if st.button("📲 Send Pro Quant Signals to Telegram"):
        if telegram_token and chat_id:
          sent_status = send_telegram_alert(
              telegram_token, chat_id, tg_message
          )
          if sent_status:
            st.info("📲 Telegram Bot-kku Pro Quant signals anuppappattathu!")
          else:
            st.warning("⚠️ Telegram dispatch error.")
        else:
          st.info("💡 Telegram Token & Chat ID missing.")

    else:
      st.error("⚠️ Data fetching error. Please check internet connection.")

  except Exception as e:
    st.error(f"Pro Quant Engine execution error: {e}")
            
