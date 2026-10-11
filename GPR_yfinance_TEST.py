import os
import math
import time
from typing import Any

import requests
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# ============================================================
# GPR STOCK SCANNER — STREAMLIT
# Data provider: Yahoo Finance via yfinance (tanpa Arjum API key).
# ============================================================

st.set_page_config(
    page_title="GPR Stock Scanner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "900"))
YF_PERIODS = {"1d": "1y", "1h": "60d", "15m": "30d", "5m": "30d"}

# Fallback only. A remote ticker directory is attempted first.
FALLBACK_CODES = """
AADI AALI ABBA ABDA ABMM ACES ACRO ACST ADCP ADES ADHI ADMF ADMG ADMR ADRO
AGAR AGII AIMS AISA AKKU AKPI AKRA AKSI ALDO ALKA ALMI ALTO AMAG AMAN AMAR
AMFG AMIN AMMN AMMS AMOR ANJT ANTM APII APIC APLI APMI ARCI ARGO ARII ARKA
ARKO ARNA ARTA ARTO ASBI ASDM ASGR ASII ASJT ASLC ASLI ASMI ASPI ASRI ASRM
ASSA ATAP AUTO AVIA AWAN AYLS BAPA BAPI BATA BAYU BBCA BBHI BBKP BBLD BBNI
BBRI BBSI BBTN BBYB BCAP BCIC BCIP BDMN BEBS BEEF BEKS BELI BELL BESS BEST
BFIN BGTG BHAT BHIT BIKA BIMA BINA BINO BIPP BIRD BISI BJBR BJTM BKDP BKSL
BKSW BLTA BLTZ BMAS BMRI BMTR BNBA BNGA BNII BNLI BOBA BOGA BOLA BOLT BRAM
BREN BRIS BRMS BRNA BRPT BSDE BSIM BSSR BTEK BTEL BTON BTPN BTPS BUDI BULL
BUMI BUVA BYAN CAMP CARE CASH CASS CBMF CBPE CCSI CEKA CENT CFIN CHEM CINT
CITA CITY CLAY CLEO CMNP CMOA CMNT CPRO CPIN CPRI CSAP CSIS CTBN CTTH CTRA
CTRA CUAN CYBR DADA DART DAYA DCII DEFI DEPO DEWA DGIK DGNS DGWG DILD DKFT
DMAS DMMX DMND DNAR DOID DPNS DPUM DRMA DSFI DSNG DSSA DUTI DVLA DWGL EAST
ECII EDGE EKAD ELIT ELSA ELTY EMDE EMTK ENAK ENRG ENZO EPAC ERAA ERAL ESIP
ESSA ESTI ETWA EURO EXCL FAPA FAST FILM FIRE FISH FITT FLMC FMII FOLK FOOD
FORU FPNI FUTR GAMA GDST GDYR GEMA GEMS GGRM GGRP GHON GIAA GJTL GLVA GMFI
GMTD GOLD GOOD GPRA GPSO GRPM GSMF GTBO GTRA GTSI GULA GUNA GWSA HADE HAIS
HATM HBAT HDFA HDTX HEAL HELI HERO HEXA HITS HKMU HOME HOTL HRME HRTA HRUM
IATA IBFN IBST IBOS ICCA ICON IDEA IFII IKAI IKAN IKBI IKPM IMAS IMJS IMPC
INAF INAI INCI INCO INDF INDR INDS INDX INDY INKP INOV INPC INPP INRU INTA
INTD INTP IPCC IPCM IPOL IPPE IPTV IRRA IRSX ISAT ISSP ITIC ITMA ITMG JARR
JAST JATI JAWA JECC JGLE JIHD JKON JMAS JPFA JRPT JSKY JSMR JTPE KAEF KAYU
KBAG KBLI KBLM KBRI KDSI KDTN KEEN KEJU KIAS KIJA KINO KIOS KKGI KLBF KMDS
KMTR KOBX KOIN KONI KOPI KPIG KREN KRYA LABA LAJU LAND LAPD LCAS LCKM LEAD
LINK LMAS LMPI LOPI LPCK LPKR LPPF LRNA LSIP LTLS LUCY MAGP MAIN MAPA MAPB
MAPI MARK MASA MASB MAYA MBAP MBSS MBTO MCAS MCOL MDIA MDKA MDKI MDLN MDRN
MEDC MEGA MERK META MFMI MGNA MGRO MICE MIDI MIKA MINA MIRA MITI MKNT MKPI
MLBI MLIA MLPL MLPT MLPT MLPT MMIX MMLP MMSI MNCN MPPA MPMX MREI MSIN MTDL
MTEL MTLA MTMH MTPS MTRA MTWI MULT MYOH MYOR MYTX NASI NATO NELY NEST NETV
NICL NIKL NIPS NISP NOBU NRCA NSSS NUSA OASA OBMD OCAP OKAS OMRE OPMS PADI
PALM PAMG PANI PANR PANS PBID PBRX PBSA PCAR PDES PEGE PEHA PGAS PGEO PGLI
PGUN PICO PJAA PKPK PLAN PLIN PMJS PMMP PMUI PNBN PNBS PNGO PNIN PNSE POLI
POLL POLU PORT POWR PPRE PPRO PRDA PRIM PSAB PSAT PSDN PSKT PTPP PUDP PURA
PURE PWON PYFA RAJA RALS RANC RBMS RDTX REAL RELI RICY RIGS RISE RMBA RMKE
ROCK RODA ROTI RUIS RUNS SAFE SAME SAMF SAPX SATU SBAT SBCS SBMA SCCO SCMA
SCNP SDMU SDPC SDRA SGRO SHID SHIP SICO SIDO SILO SIMA SIMP SIPD SKBM SKLT
SKRN SLIS SMAR SMBR SMCB SMDM SMDR SMGA SMGR SMIL SMKL SMKM SMMT SMRA SMSM
SNLK SOCI SOFA SOHO SOSS SOTS SPMA SPTO SQMI SRAJ SRTG SSIA SSMS SSTM STAR
STTP SUNI SUPR SURE SWAT SWID TALF TAMU TBIG TBLA TBMS TCID TCPI TDPM TELE
TFAS TGKA TGRA TIFA TINS TIRA TKIM TLKM TLDN TMAS TMPO TNCA TOBA TOPS TOTL
TOTO TOWR TPIA TPMA TRGU TRIL TRIM TRIN TRIO TRIS TRJA TRON TRUE TSCP TUGU
TYRE UANG UCID ULTJ UNIC UNIT UNTR UNVR VICI VINS VKTR VRNA WAPO WEGE WEHA
WIFI WIKA WINR WINS WIRG WMPP WMUU WTON YPAS ZATA ZBRA ZINC ZONE
""".split()
FALLBACK_CODES = list(dict.fromkeys(FALLBACK_CODES))


class ArjumRateLimitError(RuntimeError):
    """Compatibility alias for upstream temporary throttling."""


def extract_rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "history", "candles", "items", "stocks", "screener"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
        for value in payload.values():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                return value
    return []


@st.cache_data(ttl=3600, show_spinner=False)
def get_universe():
    """Try public stock-symbol dataset API; fallback to embedded seed list."""
    # Hugging Face datasets-server API; dataset rows are only ticker metadata,
    # not price data. If the remote schema changes, the fallback is used.
    urls = [
        "https://datasets-server.huggingface.co/rows?dataset=kjhq/Indonesia-Stock-Symbols-and-Metadata&config=default&split=train&offset=0&length=1000",
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=12)
            if response.ok:
                payload = response.json()
                rows = payload.get("rows", [])
                codes = []
                for item in rows:
                    row = item.get("row", item) if isinstance(item, dict) else {}
                    code = row.get("ticker") or row.get("symbol") or row.get("code")
                    market = str(row.get("market", ""))
                    if code and (not market or "indonesia" in market.lower() or "idx" in market.lower()):
                        code = str(code).upper().replace(".JK", "").strip()
                        if code.isalnum() and 2 <= len(code) <= 5:
                            codes.append(code)
                codes = list(dict.fromkeys(codes))
                if len(codes) >= 100:
                    return codes, "Direktori simbol publik (perlu verifikasi status listing)"
        except Exception:
            pass

    return FALLBACK_CODES.copy(), "Daftar cadangan (belum tentu lengkap/terkini)"


def normalize_history(payload):
    rows = extract_rows(payload)
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    aliases = {
        "time": ["time", "date", "datetime", "timestamp", "t"],
        "open": ["open", "o", "Open"],
        "high": ["high", "h", "High"],
        "low": ["low", "l", "Low"],
        "close": ["close", "c", "Close", "price"],
        "volume": ["volume", "vol", "v", "Volume"],
    }
    rename = {}
    for target, choices in aliases.items():
        for column in choices:
            if column in df.columns:
                rename[column] = target
                break
    df = df.rename(columns=rename)
    if "close" not in df.columns:
        return pd.DataFrame()
    for column in ("open", "high", "low"):
        if column not in df.columns:
            df[column] = df["close"]
    if "volume" not in df.columns:
        df["volume"] = 0.0
    if "time" in df.columns:
        numeric_time = pd.to_numeric(df["time"], errors="coerce")
        if numeric_time.notna().mean() > 0.8:
            unit = "ms" if numeric_time.dropna().median() > 10**11 else "s"
            df["time"] = pd.to_datetime(numeric_time, unit=unit, errors="coerce", utc=True)
        else:
            df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
        df = df.sort_values("time")
    for column in ("open", "high", "low", "close", "volume"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df.dropna(subset=["close"]).reset_index(drop=True)


def ema(series, length):
    return series.ewm(span=length, adjust=False, min_periods=1).mean()


def matern32_kernel(x, z, amplitude, scale):
    d = x - z
    distance2 = d[0]**2 + 0.8*d[1]**2 + 0.6*d[2]**2 + 0.8*d[3]**2 + 0.6*d[4]**2
    u = math.sqrt(3.0 * max(float(distance2), 0.0)) / scale
    return amplitude * (1.0 + u) * math.exp(-u)


def gpr_project(df, horizon=10, training=30, momentum_len=5, vol_len=14,
                ema_fast=8, ema_slow=21, kernel_scale=1.5, noise_ratio=0.30,
                volume_fade=0.65, atr_width=0.70):
    min_needed = max(training + vol_len + ema_slow + 10, 60)
    if len(df) < min_needed:
        raise ValueError(f"Data candle hanya {len(df)}; perlu minimal sekitar {min_needed}.")
    close = df["close"].astype(float).to_numpy()
    volume = df["volume"].fillna(0).astype(float).to_numpy()
    high = df["high"].astype(float).to_numpy()
    low = df["low"].astype(float).to_numpy()

    logret = np.full(len(close), np.nan)
    logret[1:] = np.log(np.maximum(close[1:], 1e-12) / np.maximum(close[:-1], 1e-12))
    ret_series = pd.Series(logret)
    momentum = ret_series.ewm(span=momentum_len, adjust=False, min_periods=1).mean().to_numpy()
    volatility = ret_series.rolling(vol_len, min_periods=vol_len).std(ddof=1).to_numpy()
    vol_base = pd.Series(volatility).rolling(training, min_periods=training).mean().to_numpy()
    avg_volume = pd.Series(volume).rolling(vol_len, min_periods=1).mean().to_numpy()
    rel_volume = np.zeros(len(close))
    valid = (volume > 0) & (avg_volume > 0)
    rel_volume[valid] = np.log(volume[valid] / avg_volume[valid])
    fast = ema(pd.Series(close), ema_fast).to_numpy()
    slow = ema(pd.Series(close), ema_slow).to_numpy()
    direction = (fast - slow) / np.maximum(close, 1e-12)

    prev_close = np.r_[np.nan, close[:-1]]
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    tr[0] = high[0] - low[0]
    atr = pd.Series(tr).ewm(alpha=1/vol_len, adjust=False, min_periods=vol_len).mean().to_numpy()

    idx = len(df) - 1
    vol_ref = max(float(vol_base[idx]) if np.isfinite(vol_base[idx]) else 0.0, 0.0001)
    if not np.isfinite(volatility[idx]) or not np.isfinite(atr[idx]) or not np.isfinite(logret[idx]):
        raise ValueError("Indikator belum siap pada candle terakhir.")

    X, y = [], []
    for r in range(training):
        target_idx = idx - training + 1 + r
        feature_idx = target_idx - 1
        if feature_idx < 1 or not np.isfinite(logret[target_idx]):
            continue
        X.append([
            logret[feature_idx] / vol_ref,
            momentum[feature_idx] / vol_ref,
            rel_volume[feature_idx],
            (volatility[feature_idx] / vol_ref - 1.0) if np.isfinite(volatility[feature_idx]) else 0.0,
            direction[feature_idx] / vol_ref,
        ])
        y.append(logret[target_idx])

    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n = len(y)
    if n < max(20, training - 3):
        raise ValueError("Observasi training valid terlalu sedikit.")

    signal_var = max(float(np.mean(y*y)), 1e-8)
    noise_var = signal_var * noise_ratio + 1e-10
    K = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1):
            value = matern32_kernel(X[i], X[j], signal_var, kernel_scale)
            if i == j:
                value += noise_var
            K[i, j] = K[j, i] = value
    try:
        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
    except np.linalg.LinAlgError:
        raise ValueError("Matriks GPR tidak stabil.")

    price_start = float(close[idx])
    price_prev = price_start
    ret_prev = float(logret[idx])
    mom_prev = float(momentum[idx])
    fast_prev, slow_prev = float(fast[idx]), float(slow[idx])
    volume_prev = float(rel_volume[idx])
    vol_prev = float(volatility[idx])
    cumulative_return = 0.0
    predictions = []
    # Approximate GPR posterior uncertainty for each predicted log-return.
    # The cumulative value assumes forecast errors are independent across steps;
    # it is a model-uncertainty estimate, NOT a probability of loss or success.
    cumulative_variance = 0.0

    for h in range(horizon):
        fade = volume_fade ** h
        assumed_vol = vol_ref + (vol_prev - vol_ref) * fade
        x_star = np.array([
            ret_prev / vol_ref,
            mom_prev / vol_ref,
            volume_prev * fade,
            assumed_vol / vol_ref - 1.0,
            ((fast_prev - slow_prev) / max(price_prev, 1e-12)) / vol_ref,
        ])
        kstar = np.array([matern32_kernel(X[i], x_star, signal_var, kernel_scale) for i in range(n)])
        pred_ret = float(kstar @ alpha)
        try:
            solved = np.linalg.solve(L, kstar)
            predictive_variance = max(float(signal_var - solved @ solved), 0.0)
        except (np.linalg.LinAlgError, ValueError):
            predictive_variance = 0.0
        cumulative_variance += predictive_variance
        cumulative_return += pred_ret
        price_pred = price_start * math.exp(cumulative_return)
        distance = atr_width * float(atr[idx]) * math.sqrt(h + 1.0)
        predictions.append({
            "step": h + 1,
            "price": round(price_pred, 4),
            "return_pct": round((price_pred / price_start - 1.0) * 100.0, 3),
            "upper": round(price_pred + distance, 4),
            "lower": round(max(0.0001, price_pred - distance), 4),
        })
        price_prev = price_pred
        ret_prev = pred_ret
        a_m = 2.0 / (momentum_len + 1.0)
        mom_prev = a_m * pred_ret + (1.0-a_m) * mom_prev
        a_f = 2.0 / (ema_fast + 1.0)
        a_s = 2.0 / (ema_slow + 1.0)
        fast_prev = a_f * price_pred + (1.0-a_f) * fast_prev
        slow_prev = a_s * price_pred + (1.0-a_s) * slow_prev

    latest_price = float(close[idx])
    trend = "BULLISH" if fast[idx] > slow[idx] else "BEARISH"
    mom_now = float(momentum[idx]) if np.isfinite(momentum[idx]) else 0.0
    vol_now = float(volume[idx])
    vol_avg = float(avg_volume[idx]) if np.isfinite(avg_volume[idx]) else 0.0
    rel_vol = vol_now / vol_avg if vol_avg > 0 else 0.0
    final = predictions[-1]

    return {
        "price": round(latest_price, 4),
        "trend": trend,
        "momentum": "POSITIVE" if mom_now > 0 else "NEGATIVE",
        "relative_volume": round(rel_vol, 2),
        "gpr_return_pct": final["return_pct"],
        "uncertainty_pct": round(math.sqrt(max(cumulative_variance, 0.0)) * 100.0, 2),
        "projected_price": final["price"],
        "upper": final["upper"],
        "lower": final["lower"],
        "horizon": horizon,
        "predictions": predictions,
        "as_of": str(df.iloc[idx].get("time", "")),
        "bars": len(df),
    }


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def get_history_cached(code, timeframe, cache_buster=0):
    """Fetch unadjusted OHLCV; GPR model itself is unchanged."""
    interval = {"5m": "5m", "15m": "15m", "1h": "1h", "1d": "1d"}.get(timeframe)
    if not interval:
        raise ValueError(f"Timeframe tidak dikenal: {timeframe}")
    ticker = code.upper().replace(".JK", "") + ".JK"
    try:
        raw = yf.download(
            tickers=ticker, period=YF_PERIODS[interval], interval=interval,
            auto_adjust=False, actions=False, progress=False, threads=False,
            timeout=20, group_by="column", multi_level_index=False,
        )
    except Exception as exc:
        raise RuntimeError(f"Yahoo Finance gagal mengambil {ticker}: {str(exc)[:160]}") from exc
    if raw is None or raw.empty:
        raise ValueError(f"Tidak ada histori Yahoo Finance untuk {ticker} ({interval}).")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    required = ["Open", "High", "Low", "Close", "Volume"]
    if any(col not in raw.columns for col in required):
        raise ValueError(f"Kolom OHLCV tidak lengkap untuk {ticker}: {list(raw.columns)}")
    df = raw[required].copy().reset_index()
    df.columns = [str(c).lower() for c in df.columns]
    date_col = "datetime" if "datetime" in df.columns else "date"
    df = df.rename(columns={date_col: "time"})
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["close", "volume"])
    df = df[(df["close"] > 0) & (df["volume"] >= 0)]
    if len(df) < 60:
        raise ValueError(f"Histori {ticker} hanya {len(df)} candle; perlu minimal 60.")
    return df.sort_values("time").reset_index(drop=True)


def analyze_one(code, timeframe, horizon):
    hist = get_history_cached(code, timeframe, int(time.time() // CACHE_SECONDS))
    if hist.empty:
        raise ValueError("Riwayat candle kosong atau format respons tidak dikenali.")
    result = gpr_project(hist, horizon=horizon)
    result["code"] = code
    score = max(0, min(100,
        35 * (1 if result["trend"] == "BULLISH" else 0)
        + 20 * (1 if result["momentum"] == "POSITIVE" else 0)
        + 20 * min(result["relative_volume"] / 2.0, 1.0)
        + 25 * max(0, min(result["gpr_return_pct"] / 5.0, 1.0))
    ))
    result["score"] = round(score, 1)
    result["signal"] = (
        "KANDIDAT" if result["trend"] == "BULLISH"
        and result["momentum"] == "POSITIVE"
        and result["gpr_return_pct"] > 0
        else "PANTAU" if result["gpr_return_pct"] > 0 else "HINDARI"
    )
    return result


# ---------------------------- UI ----------------------------

st.markdown("""
<style>
.block-container {padding-top:1.2rem; padding-bottom:5rem; max-width:1400px;}
[data-testid="stMetric"] {background:#111c2e; border:1px solid #2b3b53; padding:14px; border-radius:14px;}
div.stButton > button {border-radius:12px; min-height:44px; font-weight:600;}
.small-note {color:#94a3b8; font-size:0.88rem;}
</style>
""", unsafe_allow_html=True)

st.title("📈 GPR STOCK SCANNER")
st.caption("IDX · QUANT LAB | Ranking berbasis GPR, tren, momentum, dan relative volume")

with st.sidebar:
    st.header("Pengaturan pemindaian")
    timeframe_label = st.selectbox(
        "Timeframe data",
        ["Harian · uji awal", "1 jam", "15 menit", "5 menit"],
        index=0,
    )
    timeframe = {
        "Harian · uji awal": "1d",
        "1 jam": "1h",
        "15 menit": "15m",
        "5 menit": "5m",
    }[timeframe_label]
    horizon = st.selectbox("Horizon candle", [3, 5, 10, 20], index=2)
    scan_size_label = st.selectbox(
        "Jumlah saham",
        ["50 saham", "300 saham", "500 saham", "Seluruh saham tersedia"],
        index=0,
    )
    min_score = st.slider("Skor minimum yang ditampilkan", 40, 80, 40, 5)
    st.caption("Skor di bawah ambang disembunyikan dari ranking, tetapi tetap dihitung.")
    start_scan = st.button("▶ Jalankan GPR Scanner", type="primary", use_container_width=True)
    resume_scan = st.button("⏯ Lanjutkan scan yang terhenti", use_container_width=True)
    refresh_universe = st.button("↻ Muat ulang daftar saham", use_container_width=True)

if refresh_universe:
    get_universe.clear()

codes, universe_source = get_universe()
st.success("Provider: Yahoo Finance via yfinance · tanpa API key Arjum.")

if "scan_results" not in st.session_state:
    st.session_state.scan_results = []
if "scan_errors" not in st.session_state:
    st.session_state.scan_errors = []
if "scan_meta" not in st.session_state:
    st.session_state.scan_meta = {}
if "scan_queue" not in st.session_state:
    st.session_state.scan_queue = []
if "scan_cursor" not in st.session_state:
    st.session_state.scan_cursor = 0
if "scan_settings" not in st.session_state:
    st.session_state.scan_settings = {}

st.caption(f"Universe lokal: {len(codes)} kode · Sumber: {universe_source}")
st.warning(
    "Universe simbol bukan jaminan semua saham aktif/listed hari ini. "
    "Data intraday memiliki batas histori; cakupan Yahoo Finance untuk setiap saham perlu diverifikasi."
)

if start_scan or resume_scan:
    if start_scan:
        if scan_size_label == "50 saham":
            target_codes = codes[:50]
        elif scan_size_label == "300 saham":
            target_codes = codes[:300]
        elif scan_size_label == "500 saham":
            target_codes = codes[:500]
        else:
            target_codes = codes[:]
        st.session_state.scan_queue = list(target_codes)
        st.session_state.scan_cursor = 0
        st.session_state.scan_results = []
        st.session_state.scan_errors = []
        st.session_state.scan_settings = {
            "timeframe": timeframe,
            "horizon": int(horizon),
            "source": universe_source,
            "requested": len(target_codes),
        }
    elif not st.session_state.scan_queue:
        st.warning("Belum ada scan yang bisa dilanjutkan. Tekan Jalankan GPR Scanner dulu.")

    queue = st.session_state.scan_queue
    cursor = int(st.session_state.scan_cursor)
    settings = st.session_state.scan_settings
    scan_timeframe = settings.get("timeframe", timeframe)
    scan_horizon = int(settings.get("horizon", horizon))
    total = len(queue)

    if total == 0:
        st.error("Daftar kode saham kosong.")
    elif cursor >= total:
        st.success("Semua kode dalam antrean sudah diproses. Untuk scan baru, tekan Jalankan GPR Scanner.")
    else:
        progress = st.progress(cursor / total, text=f"Memulai scan otomatis dari {cursor}/{total}…")
        status_box = st.empty()
        request_pause = max(0.2, min(float(os.getenv("YF_REQUEST_PAUSE", "0.5")), 5.0))
        batch_size = max(1, min(int(os.getenv("YF_BATCH_SIZE", "10")), 50))
        rate_limited = False
        processed_this_run = 0
        current_batch_end = min(total, cursor + batch_size)
        status_box.info(f"Mode otomatis aktif · batch {cursor // batch_size + 1} · target {total} saham.")

        # Auto-continue across batches in the same run. Batch boundaries only
        # update progress; the user does not need to press Resume each time.
        for pos in range(cursor, total):
            code = queue[pos]
            try:
                result = analyze_one(code, scan_timeframe, scan_horizon)
                st.session_state.scan_results = [
                    item for item in st.session_state.scan_results if item.get("code") != code
                ] + [result]
                st.session_state.scan_errors = [
                    item for item in st.session_state.scan_errors if item.get("code") != code
                ]
            except Exception as exc:
                st.session_state.scan_errors = [
                    item for item in st.session_state.scan_errors if item.get("code") != code
                ] + [{"code": code, "error": str(exc)[:220]}]

            st.session_state.scan_cursor = pos + 1
            cursor = pos + 1
            processed_this_run += 1
            progress.progress(cursor / total, text=f"Memproses {cursor}/{total}: {code}")

            if cursor % batch_size == 0 or cursor == total:
                status_box.info(
                    f"Batch otomatis selesai · {cursor}/{total} · berhasil "
                    f"{len(st.session_state.scan_results)} · error "
                    f"{len(st.session_state.scan_errors)} · lanjut otomatis…"
                )
            if cursor < total:
                time.sleep(request_pause)

        st.session_state.scan_results.sort(
            key=lambda item: (item["score"], item["gpr_return_pct"]), reverse=True
        )
        st.session_state.scan_meta = {
            **settings,
            "processed": st.session_state.scan_cursor,
            "success": len(st.session_state.scan_results),
            "errors": len(st.session_state.scan_errors),
            "not_processed": max(0, total - st.session_state.scan_cursor),
            "stopped_for_rate_limit": rate_limited,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "batch_size": batch_size,
            "automatic_batches": True,
        }
        progress.progress(1.0, text="Pemindaian selesai.")
        status_box.success(
            f"Selesai: {len(st.session_state.scan_results)} berhasil dianalisis dari {total} kode. "
            f"Error: {len(st.session_state.scan_errors)}."
        )

results = st.session_state.scan_results
errors = st.session_state.scan_errors
meta = st.session_state.scan_meta
if st.session_state.scan_queue and st.session_state.scan_cursor < len(st.session_state.scan_queue):
    st.info(
        f"Antrean scan: {st.session_state.scan_cursor}/{len(st.session_state.scan_queue)} kode selesai. "
        "Hasil parsial tersimpan di sesi ini. Tekan tombol Lanjutkan hanya jika proses sebelumnya terhenti."
    )

qualified = [item for item in results if float(item.get("score", 0)) >= min_score]
candidates = [item for item in qualified if item.get("signal") == "KANDIDAT"]
best_return = max((float(item["gpr_return_pct"]) for item in qualified), default=None)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Saham berhasil dianalisis", len(results))
m2.metric("Ranking lolos skor", len(qualified))
m3.metric("Kandidat", len(candidates))
m4.metric("Return GPR tertinggi", f"{best_return:+.2f}%" if best_return is not None else "—")

tab_rank, tab_analysis, tab_status = st.tabs(["📋 Ranking saham", "📈 Analisis saham", "ℹ️ Status data"])

with tab_rank:
    st.subheader("Ranking saham — MEDIUM ke atas")
    search = st.text_input("Cari kode saham", placeholder="Contoh: BBCA")
    display = [
        item for item in qualified
        if search.strip().upper() in item["code"].upper()
    ]
    display.sort(key=lambda item: (item["score"], item["gpr_return_pct"]), reverse=True)

    if not display:
        st.info("Belum ada saham yang memenuhi skor minimum. Jalankan scan atau turunkan ambang skor.")
    else:
        view_rows = []
        for rank, item in enumerate(display, start=1):
            score = float(item["score"])
            category = "HIGH" if score >= 80 else "MEDIUM–HIGH" if score >= 60 else "MEDIUM"
            view_rows.append({
                "Rank": rank,
                "Kode": item["code"],
                "Kategori": category,
                "Skor": score,
                "GPR Return": item["gpr_return_pct"],
                "Uncertainty (%)": item.get("uncertainty_pct", np.nan),
                "Tren": item["trend"],
                "Momentum": item["momentum"],
                "Rel. Volume": item["relative_volume"],
                "Sinyal": item["signal"],
                "Harga": item["price"],
            })
        st.caption(
            "Uncertainty (%) = perkiraan ketidakpastian prediksi GPR kumulatif untuk horizon terpilih. "
            "Ini bukan probabilitas harga turun/naik dan bukan jaminan hasil. Nilai lebih rendah "
            "berarti model lebih yakin secara relatif, bukan berarti prediksi pasti benar."
        )
        st.dataframe(pd.DataFrame(view_rows), use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Unduh ranking CSV",
            data=pd.DataFrame(view_rows).to_csv(index=False).encode("utf-8"),
            file_name="gpr_stock_ranking.csv",
            mime="text/csv",
        )

with tab_analysis:
    st.subheader("Detail proyeksi GPR")
    available_codes = [item["code"] for item in results]
    if not available_codes:
        st.info("Jalankan scan terlebih dahulu.")
    else:
        default_code = selected_default = (
            st.session_state.get("selected_code")
            if st.session_state.get("selected_code") in available_codes
            else available_codes[0]
        )
        code = st.selectbox("Pilih saham", available_codes, index=available_codes.index(default_code))
        st.session_state.selected_code = code
        item = next((entry for entry in results if entry["code"] == code), None)
        if item:
            a, b, c, d = st.columns(4)
            a.metric("Harga terakhir", f"{item['price']:,.2f}")
            b.metric("Tren", item["trend"])
            c.metric("Momentum", item["momentum"])
            d.metric("GPR Return", f"{item['gpr_return_pct']:+.2f}%")
            st.metric("GPR Uncertainty (perkiraan)", f"{item.get('uncertainty_pct', float('nan')):.2f}%")
            preds = item.get("predictions", [])
            if preds:
                chart_df = pd.DataFrame({
                    "Candle": ["Sekarang"] + [f"+{p['step']}" for p in preds],
                    "Harga": [item["price"]] + [p["price"] for p in preds],
                }).set_index("Candle")
                st.line_chart(chart_df)
                st.dataframe(pd.DataFrame(preds), use_container_width=True, hide_index=True)

with tab_status:
    st.subheader("Status koneksi dan hasil scan")
    st.write("**API key:**", "Tidak diperlukan")
    st.write("**Provider:** Yahoo Finance (yfinance)")
    st.write("**Universe:**", universe_source)
    st.write("**Jumlah kode universe:**", len(codes))
    if meta:
        st.json(meta)
    else:
        st.info("Belum ada scan pada sesi ini.")
    st.caption(
        "Yahoo Finance tidak menjamin setiap kode memiliki data. "
        "Sinyal dan proyeksi bersifat eksperimental, bukan jaminan keuntungan."
    )
    if errors:
        st.subheader(f"Kode gagal ({len(errors)})")
        error_df = pd.DataFrame(errors)
        if "error" in error_df.columns:
            error_df["jenis_error"] = error_df["error"].apply(
                lambda message: (
                    "Rate limit (429)" if "429" in str(message) or "Too Many Requests" in str(message)
                    else "Data candle kosong/format" if "candle kosong" in str(message).lower() or "format respons" in str(message).lower()
                    else "Data candle kurang" if "perlu minimal" in str(message).lower()
                    else "Koneksi/timeout" if "timeout" in str(message).lower() or "koneksi" in str(message).lower()
                    else "Error lainnya"
                )
            )
            st.caption("Ringkasan jenis error")
            st.dataframe(
                error_df["jenis_error"].value_counts().rename_axis("Jenis error").reset_index(name="Jumlah"),
                use_container_width=True,
                hide_index=True,
            )
        st.dataframe(error_df, use_container_width=True, hide_index=True)
