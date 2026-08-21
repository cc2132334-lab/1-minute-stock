import os
import time
from datetime import datetime
import pytz
import requests

# --- TELEGRAM CONFIG ---
BOT_TOKEN = "8626042409:AAHElsiJD8_Jk9R7r5VHUj8fPjcl8Meacp4"
CHAT_ID = "706694019"

# Complete NSE F&O Stocks List
FNO_STOCKS = [
    "AARTIIND.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ACC.NS",
    "ADANIENT.NS", "ADANIPORTS.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS",
    "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "ATUL.NS",
    "AUBANK.NS", "AUROPHARMA.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS",
    "BAJFINANCE.NS", "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS",
    "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS",
    "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", "BSOFT.NS",
    "CANBK.NS", "CANFINHOME.NS", "CHAMBLFERT.NS", "CHOLAFIN.NS", "CIPLA.NS",
    "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS",
    "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "DABUR.NS", "DALBHARAT.NS",
    "DEEPAKNTR.NS", "DELTACORP.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "GAIL.NS",
    "GLENMARK.NS", "GMRINFRA.NS", "GNFC.NS", "GODREJCP.NS", "GODREJPROP.NS",
    "GRANULES.NS", "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HAVELLS.NS", "HCLTECH.NS",
    "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS",
    "ICICIPRULI.NS", "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDHOTEL.NS",
    "INDIACEM.NS", "INDIAMART.NS", "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS",
    "INFY.NS", "IOC.NS", "IPCALAB.NS", "IRCTC.NS", "ITC.NS", "JINDALSTEL.NS",
    "JKCEMENT.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", "LALPATHLAB.NS",
    "LAURUSLABS.NS", "LICHSGFIN.NS", "LT.NS", "LTIM.NS", "LTTS.NS", "LUPIN.NS",
    "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MCDOWELL-N.NS",
    "MCX.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS",
    "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAUKRI.NS", "NAVINFLUOR.NS",
    "NESTLEIND.NS", "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "OFSS.NS", "ONGC.NS",
    "PAGEIND.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PIDILITIND.NS",
    "PIIND.NS", "PNB.NS", "POLYCAB.NS", "POWERGRID.NS", "PVRINOX.NS", "RAMCOCEM.NS",
    "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SAIL.NS", "SBICARD.NS", "SBILIFE.NS",
    "SBIN.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SRF.NS", "SUNPHARMA.NS",
    "SUNTV.NS", "SYNGENE.NS", "TATACHEM.NS", "TATACOMM.NS", "TATACONSUM.NS",
    "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS",
    "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS",
    "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS", "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS", "ZYDUSLIFE.NS"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def send_telegram(text_msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text_msg, "parse_mode": "Markdown"}
    for _ in range(5):
        try:
            r = requests.post(url, data=payload, timeout=15)
            if r.status_code == 200:
                print("Delivered to Telegram!")
                return True
        except Exception:
            time.sleep(3)
    return False

def get_chart_data(symbol, interval="1m", range_str="2d"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_str}"
    res = requests.get(url, headers=HEADERS, timeout=8).json()
    result = res['chart']['result'][0]
    return result.get('timestamp', []), result['indicators']['quote'][0]

def main():
    ist = pytz.timezone('Asia/Kolkata')
    today_str = datetime.now(ist).strftime("%Y-%m-%d")
    
    cpr_volume_hits = []
    pure_volume_hits = []

    print(f"[{datetime.now(ist).strftime('%H:%M:%S')}] Scanning 1st 1-Minute Candle (09:15 - 09:16)...")

    for ticker in FNO_STOCKS:
        try:
            # 1-Minute Data
            ts_1m, quotes_1m = get_chart_data(ticker, "1m", "2d")
            # 1-Day Data for CPR
            _, quotes_1d = get_chart_data(ticker, "1d", "5d")

            vols_1m = quotes_1m.get('volume', [])
            closes_1m = quotes_1m.get('close', [])

            # Target 09:15 Candle (First 1-min candle of today)
            target_idx = None
            for idx, ts in enumerate(ts_1m):
                dt = datetime.fromtimestamp(ts, ist)
                if dt.strftime("%Y-%m-%d") == today_str and dt.hour == 9 and dt.minute == 15:
                    target_idx = idx
                    break

            if target_idx is None:
                if len(vols_1m) < 22:
                    continue
                target_idx = len(vols_1m) - 1

            candle_vol = vols_1m[target_idx]
            ltp = closes_1m[target_idx]

            # 20-Period Avg 1-min Volume prior to that candle
            past_vols = [v for v in vols_1m[max(0, target_idx - 20):target_idx] if v is not None]
            if len(past_vols) < 10 or not candle_vol or not ltp:
                continue

            avg_vol_20 = sum(past_vols) / len(past_vols)
            if avg_vol_20 == 0:
                continue

            vol_ratio = candle_vol / avg_vol_20
            clean_name = ticker.replace(".NS", "")

            # Previous Day Daily CPR Calculation
            highs_1d = [h for h in quotes_1d['high'] if h is not None]
            lows_1d = [l for l in quotes_1d['low'] if l is not None]
            closes_1d = [c for c in quotes_1d['close'] if c is not None]

            is_narrow = False
            if len(highs_1d) >= 2:
                ph, pl, pc = highs_1d[-2], lows_1d[-2], closes_1d[-2]
                pivot = (ph + pl + pc) / 3
                bc = (ph + pl) / 2
                tc = (pivot - bc) + pivot
                
                # Check for tight/overlapping range (< 0.15% width)
                is_narrow = (abs(tc - bc) / pivot) * 100 <= 0.15

            # 5x Volume Condition
            if vol_ratio >= 5.0:
                item = f"• *{clean_name}* ➔ Spike: `{vol_ratio:.1f}x` | Price: `₹{ltp:.2f}`"
                if is_narrow:
                    cpr_volume_hits.append(item)
                else:
                    pure_volume_hits.append(item)

        except Exception:
            continue

    date_str = datetime.now(ist).strftime("%d-%b-%Y")
    report = (
        f"🎯 *1-MIN MORNING BREAKOUT REPORT*\n"
        f"🗓 *Date:* {date_str}\n"
        f"⏱ *Timeframe:* 1-Min (09:15 - 09:16 Candle)\n\n"
        f"🔥 *1. NARROW CPR + 5X VOLUME SPIKE:*\n"
    )
    report += "\n".join(cpr_volume_hits) if cpr_volume_hits else "_No stocks matched this setup today._"
    
    report += "\n\n🚨 *2. PURE 5X VOLUME SPIKE:*\n"
    report += "\n".join(pure_volume_hits) if pure_volume_hits else "_No stocks matched pure volume setup._"

    send_telegram(report)

if __name__ == "__main__":
    main()
