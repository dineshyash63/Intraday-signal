import requests
import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Page Configuration
st.set_page_config(
    page_title="Ultra-Advanced Next-Gen AI Intraday Engine",
    page_icon="🤖",
    layout="wide",
)

# Auto-refresh every 30 seconds for live market synchronization
count = st_autorefresh(interval=30000, key="nextgen_ai_auto_refresh")

st.title("🤖 Ultra-Advanced Next-Gen AI Intraday Quant Engine")
st.write(
    "வணக்கம் நண்பா! எந்தச் சூழ்நிலையிலும் (Market எப்படி இருந்தாலும்) தவிர்க்காமல்"
    " எப்போதும் Top 3 பெஸ்ட் இன்ட்ராடே சிக்னல்களைத் தரும் எக்ஸ்ட்ரீம் AI இன்டெலிஜென்ட்"
    " சிஸ்டம்."
)

# --- Sidebar: AI Quant Controls & Settings ---
st.sidebar.header("🛠️ Next-Gen AI Quant Hub")

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
st.sidebar.info(f"AI Dynamic Max Risk Per Trade: ₹{allowed_loss:.2f}")

st.sidebar.markdown("---")
st.subheader("🔥 High-Liquidity Nifty F&O AI Universe")

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


# Advanced AI Intelligence Engine Scan (Guaranteed 3 Signals Logic)
with st.spinner(
    "🤖 Next-Gen AI is analyzing market flows to extract guaranteed Top 3"
    " signals..."
):
  try:
    scored_stocks = []

    for symbol in watchlist:
      try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="60d", interval="1d")

        if df is not None and not df.empty and len(df) >= 30:
          df = df.dropna(subset=["Close", "High", "Low", "Volume"])
          if len(df) < 30:
            continue

          latest_price = float(df["Close"].iloc[-1])
          prev_close = float(df["Close"].iloc[-2])
          vol = int(df["Volume"].iloc[-1])
          avg_vol_20 = float(df["Volume"].rolling(window=20).mean().iloc[-1])

          # Indicators
          ema_9 = float(df["Close"].ewm(span=9, adjust=False).mean().iloc[-1])
          ema_21 = float(df["Close"].ewm(span=21, adjust=False).mean().iloc[-1])

          delta = df["Close"].diff()
          gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
          loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
          rs = gain / loss
          rsi_series = 100 - (100 / (1 + rs))
          current_rsi = float(rsi_series.iloc[-1])

          exp1 = df["Close"].ewm(span=12, adjust=False).mean()
          exp2 = df["Close"].ewm(span=26, adjust=False).mean()
          macd = exp1 - exp2
          signal_line = macd.ewm(span=9, adjust=False).mean()
          current_hist = float((macd - signal_line).iloc[-1])

          high_low = df["High"] - df["Low"]
          high_close = (df["High"] - df["Close"].shift()).abs()
          low_close = (df["Low"] - df["Close"].shift()).abs()
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

          # Guaranteed Logic: Dynamic Buy/Sell classification based on momentum/price position
          if latest_price >= ema_9:
            direction = "AI STRONG BUY (LONG)"
            sl_numeric = latest_price - (1.1 * atr)
            target_1 = latest_price + (1.6 * atr)
            target_2 = latest_price + (2.6 * atr)
            entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 1.002):.2f}"
            ai_score = (
                (current_rsi * 1.5)
                + (abs(price_change_pct) * 10)
                + (volume_spike_ratio * 10)
            )
            ai_reason = (
                f"Bullish Momentum Zone (Price >= EMA 9), RSI ({current_rsi:.1f})"
                f", Volume Strength ({volume_spike_ratio:.1f}x)"
            )
          else:
            direction = "AI STRONG SELL (SHORT)"
            sl_numeric = latest_price + (1.1 * atr)
            target_1 = latest_price - (1.6 * atr)
            target_2 = latest_price - (2.6 * atr)
            entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 0.998):.2f}"
            ai_score = (
                ((100 - current_rsi) * 1.5)
                + (abs(price_change_pct) * 10)
                + (volume_spike_ratio * 10)
            )
            ai_reason = (
                f"Bearish Momentum Zone (Price < EMA 9), RSI ({current_rsi:.1f})"
                f", Volume Strength ({volume_spike_ratio:.1f}x)"
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
              "qty": suggested_qty,
              "vol": vol,
              "vol_ratio": volume_spike_ratio,
              "reason": ai_reason,
          })
      except Exception:
        continue

    if scored_stocks:
      # Sort by AI Intelligence Score to get absolute best 3
      scored_stocks.sort(key=lambda x: x["score"], reverse=True)
      top_3_stocks = scored_stocks[:3]

      st.success(
          "🤖 Next-Gen AI Scan Completed! Guaranteed Top 3 Intraday Signals"
          " Generated."
      )
      st.markdown("---")
      st.markdown("### 🏆 Guaranteed Top 3 AI Signals:")

      tg_message = "🤖 *GUARANTEED TOP 3 AI INTRADAY SIGNALS* 🤖\n\n"

      for i, stock in enumerate(top_3_stocks, 1):
        with st.container():
          st.markdown(
              f"### 🚀 Rank {i}: {stock['symbol']} ({stock['direction']})"
          )
          st.info(f"🧠 **AI Intelligence Analysis:** {stock['reason']}")

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
          col2.write(f"**Optimized Qty:** {stock['qty']} Shares")

          col3.markdown(f"**Target 1:** {stock['target1']}")
          col3.markdown(f"**Target 2:** {stock['target2']}")
          col3.write(
              f"Vol Ratio: {stock['vol_ratio']:.1f}x | AI Score:"
              f" {stock['score']:.1f}"
          )
          st.markdown("---")

        tg_message += (
            f"*Rank {i}: {stock['symbol']}* ({stock['direction']})\n"
            f"🧠 AI Analysis: {stock['reason']}\n"
            f"💰 Price: ₹{stock['price']:.2f} | RSI: {stock['rsi']:.1f}\n"
            f"🎯 Entry: {stock['entry']}\n"
            f"🛡️ SL: {stock['sl']} | Qty: {stock['qty']}\n"
            f"🎯 T1: {stock['target1']} | T2: {stock['target2']}\n\n"
        )

      tg_message += "_Powered by Next-Gen AI Quant Engine_ 🤖"

      if st.button("📲 Send Guaranteed AI Signals to Telegram"):
        if telegram_token and chat_id:
          sent_status = send_telegram_alert(
              telegram_token, chat_id, tg_message
          )
          if sent_status:
            st.info("📲 Telegram Bot-kku top 3 AI signals anuppappattathu!")
          else:
            st.warning("⚠️ Telegram dispatch error.")
        else:
          st.info("💡 Telegram Token & Chat ID missing.")

    else:
      st.error("⚠️ Data fetching error. Please check internet or refresh.")

  except Exception as e:
    st.error(f"Next-Gen AI Engine execution error: {e}")
            
