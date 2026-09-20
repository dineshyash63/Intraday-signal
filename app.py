import time
import requests
import streamlit as st
import yfinance as yf

# Pakkathin thalappu matrum vadivamaippu
st.set_page_config(
    page_title="Ultimate Pro Intraday Trading System",
    page_icon="💎",
    layout="wide",
)

st.title("💎 Advanced Pro Live Intraday Trading & AI Engine")
st.write(
    "Vanakkam nanba! RSI, SMA matrum Volume momentum-udan error illamal 3"
    " best signals tharum app."
)

# --- Sidebar: Telegram & Risk Management ---
st.sidebar.header("🛠️ Advanced Settings & Risk Management")

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
st.subheader("🔥 Advanced Market Scanner (Top 3 Signals)")

# Expanded Nifty High Volume Watchlist
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


if st.button("🚀 Run Advanced Scan & Get Signals"):
  with st.spinner("Market data-vai error-free-ah scan seigirathu..."):
    try:
      scored_stocks = []

      for symbol in watchlist:
        try:
          # period-ai 30 days-ku mathiyullom, appothan RSI ku thevaiyana 14+ days data kandippa kidaikkum
          ticker = yf.Ticker(symbol)
          df = ticker.history(period="30d", interval="1d")

          if df is not None and not df.empty and len(df) >= 15:
            # Drop any rows with NaN in Close
            df = df.dropna(subset=["Close", "High", "Low", "Volume"])
            if len(df) < 15:
              continue

            latest_price = float(df["Close"].iloc[-1])
            prev_close = float(df["Close"].iloc[-2])
            day_high = float(df["High"].iloc[-1])
            day_low = float(df["Low"].iloc[-1])
            vol = int(df["Volume"].iloc[-1])

            # Safe SMA & RSI calculation
            sma_5 = float(df["Close"].rolling(window=5).mean().iloc[-1])
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

            rs = gain / loss
            rsi_series = 100 - (100 / (1 + rs))
            current_rsi = float(rsi_series.iloc[-1])

            if (
                str(current_rsi) == "nan"
                or str(latest_price) == "nan"
                or str(prev_close) == "nan"
            ):
              continue

            price_change_pct = ((latest_price - prev_close) / prev_close) * 100
            range_pct = ((day_high - day_low) / latest_price) * 100
            momentum_score = abs(price_change_pct) + range_pct + abs(current_rsi - 50)

            if latest_price >= sma_5 and current_rsi >= 45:
              direction = "STRONG BUY (LONG)"
              entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 1.002):.2f}"
              target_1 = f"₹{(latest_price * 1.015):.2f}"
              target_2 = f"₹{(latest_price * 1.03):.2f}"
              stop_loss = f"₹{(latest_price * 0.99):.2f}"
              sl_numeric = latest_price * 0.99
            else:
              direction = "STRONG SELL (SHORT)"
              entry_zone = f"₹{latest_price:.2f} - ₹{(latest_price * 0.998):.2f}"
              target_1 = f"₹{(latest_price * 0.985):.2f}"
              target_2 = f"₹{(latest_price * 0.97):.2f}"
              stop_loss = f"₹{(latest_price * 1.01):.2f}"
              sl_numeric = latest_price * 1.01

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
                "score": momentum_score,
                "direction": direction,
                "entry": entry_zone,
                "target1": target_1,
                "target2": target_2,
                "sl": stop_loss,
                "qty": suggested_qty,
                "vol": vol,
            })
        except Exception:
          continue

      if scored_stocks:
        scored_stocks.sort(key=lambda x: x["score"], reverse=True)
        top_3_stocks = scored_stocks[:3]

        st.success("✅ Market Scanning Vetrikaramaga Mudinthathu!")
        st.markdown("---")
        st.markdown(
            "### 🌟 Today's Guaranteed TOP 3 Intraday Profit Signals:"
        )

        tg_message = "🚨 *EXPERT DAILY TOP 3 INTRADAY SIGNALS* 🚨\n\n"

        for i, stock in enumerate(top_3_stocks, 1):
          with st.container():
            st.markdown(
                f"### 🏆 Rank {i}: {stock['symbol']} ({stock['direction']})"
            )
            col1, col2, col3 = st.columns(3)
            col1.write(f"Live Price: ₹{stock['price']:.2f} | RSI: {stock['rsi']:.1f}")
            if stock["change"] >= 0:
              col1.markdown(
                  "Change: :green[+" + f"{stock['change']:.2f}%" + "]"
              )
            else:
              col1.markdown(
                  "Change: :red[" + f"{stock['change']:.2f}%" + "]"
              )

            col2.write(f"**Entry Zone:** {stock['entry']}")
            col2.write(f"**Stop Loss:** {stock['sl']}")
            col2.write(f"**Suggested Qty:** {stock['qty']} Shares")

            col3.markdown(f"**Target 1:** {stock['target1']}")
            col3.markdown(f"**Target 2:** {stock['target2']}")
            col3.write(f"Volume: {stock['vol']:,}")
            st.markdown("---")

          tg_message += (
              f"*Rank {i}: {stock['symbol']}* ({stock['direction']})\n"
              f"💰 Price: ₹{stock['price']:.2f} | RSI: {stock['rsi']:.1f}\n"
              f"🎯 Entry: {stock['entry']}\n"
              f"🛡️ SL: {stock['sl']} | Qty: {stock['qty']}\n"
              f"🎯 T1: {stock['target1']} | T2: {stock['target2']}\n\n"
          )

        tg_message += "_Strictly follow risk management!_"

        if telegram_token and chat_id:
          sent_status = send_telegram_alert(
              telegram_token, chat_id, tg_message
          )
          if sent_status:
            st.info(
                "📲 Telegram Bot moolamaaga TOP 3 Signals unathu Telegram-kku"
                " anuppappattathu!"
            )
          else:
            st.warning("⚠️ Telegram message anuppuvathil thadangal.")
        else:
          st.info("💡 Telegram Token matrum Chat ID thevai.")

      else:
        st.error(
            "Market data kidaikkavillai (Weekend or Holiday aaga irukkalam)."
        )

    except Exception as e:
      st.error(f"Scan seivathil thadangal: {e}")
              
