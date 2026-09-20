import time
import requests
import streamlit as st
import yfinance as yf

# Pakkathin thalappu matrum vadivamaippu
st.set_page_config(
    page_title="Ultimate 3-Signals Intraday Profit Engine",
    page_icon="💎",
    layout="wide",
)

st.title("💎 Ultimate Pro Live Intraday Profit Engine (Daily Top 3 Signals)")
st.write(
    "Vanakkam nanba! Live market data-vai scan panni, oru nalukku"
    " kandippaaga **3 Best Intraday Trade Signals**-ai tharuvathodu, adhai"
    " Telegram-kku anuppum prathyega app."
)

# --- Sidebar: Telegram & Risk Management ---
st.sidebar.header("🛠️ Telegram & Risk Management")

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
capital = st.sidebar.number_input("Motham muthaleedu (Capital ₹)", value=25000)
risk_pct = st.sidebar.slider("Erkkum nashtam sathavigam (%)", 0.5, 3.0, 1.0)
allowed_loss = (capital * risk_pct) / 100
st.sidebar.info(f"Athigabatcha erkkakkoodiya nashtam: ₹{allowed_loss:.2f}")

auto_refresh = st.sidebar.checkbox(
    "🔄 Auto-Refresh Live Data (Every 60 Seconds)", value=False
)
if auto_refresh:
  time.sleep(60)
  st.rerun()

st.sidebar.markdown("---")
st.subheader("🔥 Daily Top 3 Market Scanner")

# Expanded Nifty 50 High Volume Watchlist
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


if st.button("🚀 Run Scan & Get Top 3 Trade Signals"):
  with st.spinner("Market data-vai aayvu seithu Top 3 signals edukkirathu..."):
    try:
      scored_stocks = []

      for symbol in watchlist:
        try:
          ticker = yf.Ticker(symbol)
          df = ticker.history(period="5d", interval="1d")
          if not df.empty and len(df) >= 2:
            latest_price = df["Close"].iloc[-1]
            prev_close = df["Close"].iloc[-2]
            day_high = df["High"].iloc[-1]
            day_low = df["Low"].iloc[-1]
            vol = df["Volume"].iloc[-1]

            price_change_pct = ((latest_price - prev_close) / prev_close) * 100
            range_pct = ((day_high - day_low) / latest_price) * 100
            momentum_score = abs(price_change_pct) + range_pct

            if price_change_pct >= 0:
              direction = "BUY (LONG)"
              entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 1.002):.2f}"
              target_1 = f"₹{(latest_price * 1.015):.2f}"
              target_2 = f"₹{(latest_price * 1.03):.2f}"
              stop_loss = f"₹{(latest_price * 0.99):.2f}"
            else:
              direction = "SELL (SHORT)"
              entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 0.998):.2f}"
              target_1 = f"₹{(latest_price * 0.985):.2f}"
              target_2 = f"₹{(latest_price * 0.97):.2f}"
              stop_loss = f"₹{(latest_price * 1.01):.2f}"

            scored_stocks.append({
                "symbol": symbol.replace(".NS", ""),
                "price": latest_price,
                "change": price_change_pct,
                "score": momentum_score,
                "direction": direction,
                "entry": entry_zone,
                "target1": target_1,
                "target2": target_2,
                "sl": stop_loss,
                "vol": vol,
            })
        except Exception:
          continue

      if scored_stocks:
        # Sort by momentum score to get top stocks
        scored_stocks.sort(key=lambda x: x["score"], reverse=True)

        # Select top 3 stocks guaranteed
        top_3_stocks = scored_stocks[:3]

        st.success("✅ Market Scanning Vetrikaramaga Mudinthathu!")
        st.markdown("---")
        st.markdown(
            "### 🌟 Today's Guaranteed TOP 3 Intraday Profit Trade Signals:"
        )

        tg_message = (
            f"🚨 *EXPERT DAILY TOP 3 INTRADAY SIGNALS* 🚨\n\n"
        )

        for i, stock in enumerate(top_3_stocks, 1):
          with st.container():
            st.markdown(
                f"### 🏆 Rank {i}: {stock['symbol']} ({stock['direction']})"
            )
            col1, col2, col3 = st.columns(3)
            col1.write(f"Live Price: ₹{stock['price']:.2f}")
            if stock["change"] >= 0:
              col1.markdown(
                  "Change: :green[+" + f"{stock['change']:.2f}%" + "]"
              )
            else:
              col1.markdown("Change: :red[" + f"{stock['change']:.2f}%" + "]")

            col2.write(f"**Entry Zone:** {stock['entry']}")
            col2.write(f"**Stop Loss:** {stock['sl']}")

            col3.markdown(f"**Target 1:** {stock['target1']}")
            col3.markdown(f"**Target 2:** {stock['target2']}")
            col3.write(f"Volume: {stock['vol']:,}")
            st.markdown("---")

          # Build Telegram message content for all top 3
          tg_message += (
              f"*Rank {i}: {stock['symbol']}* ({stock['direction']})\n"
              f"💰 Price: ₹{stock['price']:.2f} | Chg: {stock['change']:.2f}%\n"
              f"🎯 Entry: {stock['entry']}\n"
              f"🛡️ SL: {stock['sl']}\n"
              f"🎯 T1: {stock['target1']} | T2: {stock['target2']}\n\n"
          )

        tg_message += "_Strictly follow risk management!_"

        # Send all 3 signals in a single Telegram alert
        if telegram_token and chat_id:
          sent_status = send_telegram_alert(
              telegram_token, chat_id, tg_message
          )
          if sent_status:
            st.info(
                "📲 Telegram Bot moolamaaga **TOP 3 Signals** unathu"
                " Telegram-kku anuppappattathu!"
            )
          else:
            st.warning(
                "⚠️ Telegram message anuppuvathil thadangal. Bot /start"
                " cheythal enru parthidaavum."
            )
        else:
          st.info("💡 Telegram Token matrum Chat ID thevai.")

      else:
        st.error("Market data kidaikkavillai.")

    except Exception as e:
      st.error(f"Scan seivathil thadangal: {e}")
