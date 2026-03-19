import io
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(page_title="Crypto Dashboard Pro", layout="wide")

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
    [data-testid="stMain"], .main, section.main {
        background-color: #080c14 !important;
        color: #e8ecf0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stSidebar"] { background-color: #0d1117 !important; }

    .block-container {
        padding-top: 0 !important;
        padding-bottom: 3rem;
        max-width: 1440px;
        background-color: #080c14 !important;
    }

    /* ── Streamlit widget overrides ── */
    [data-testid="stSelectbox"] > div > div {
        background-color: #12192a !important;
        color: #e8ecf0 !important;
        border: 1px solid #1e2d45 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }
    label, .stSelectbox label, .stTextInput label {
        color: #6b7a99 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.4px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stButton"] button {
        background: linear-gradient(135deg, #1a6bff 0%, #0d4fd6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 1.2rem !important;
        transition: opacity 0.2s !important;
    }
    [data-testid="stButton"] button:hover { opacity: 0.85 !important; }

    /* ── Tab bar ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #1a2540 !important;
        gap: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        color: #6b7a99 !important;
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        margin: 0 !important;
        transition: color 0.2s, border-color 0.2s !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #1a6bff !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-panel"] {
        background: transparent !important;
        padding: 1.5rem 0 0 0 !important;
    }

    /* ── Hero / page header ── */
    .page-hero {
        background: linear-gradient(135deg, #0d1a35 0%, #080c14 60%, #0a1020 100%);
        border-bottom: 1px solid #1a2540;
        padding: 2rem 2.5rem 1.8rem;
        margin: 0 -1rem 1.5rem;
    }
    .page-hero h1 {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0 0 0.3rem;
        letter-spacing: -0.5px;
    }
    .page-hero .sub {
        color: #6b7a99;
        font-size: 0.92rem;
        font-weight: 500;
    }
    .page-hero .sub span {
        color: #1a6bff;
        font-weight: 600;
    }

    /* ── Controls bar ── */
    .controls-bar {
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        display: flex;
        gap: 1rem;
        align-items: flex-end;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.15s;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #1a6bff, #00c6ff);
        border-radius: 16px 16px 0 0;
    }
    .metric-card:hover { border-color: #2a4080; transform: translateY(-2px); }
    .metric-title {
        font-size: 0.75rem;
        color: #6b7a99;
        font-weight: 600;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }
    .metric-value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .metric-value-small {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
        letter-spacing: -0.3px;
    }

    /* ── Section boxes ── */
    .section-box {
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        margin-top: 1.2rem;
    }
    .section-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #6b7a99;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title::after {
        content: "";
        flex: 1;
        height: 1px;
        background: #1a2540;
    }

    /* ── Signal badges ── */
    .rec-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.45rem 1.1rem;
        border-radius: 999px;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .rec-buy  { background: rgba(0,200,83,0.15);  color: #00e676; border: 1px solid rgba(0,200,83,0.3); }
    .rec-sell { background: rgba(255,82,82,0.15); color: #ff5252; border: 1px solid rgba(255,82,82,0.3); }
    .rec-wait { background: rgba(255,152,0,0.15); color: #ffb74d; border: 1px solid rgba(255,152,0,0.3); }

    /* ── Sentiment colors ── */
    .signal-bull    { color: #00e676; font-weight: 700; }
    .signal-bear    { color: #ff5252; font-weight: 700; }
    .signal-neutral { color: #ffb74d; font-weight: 700; }
    .small-note { color: #6b7a99; font-size: 0.88rem; line-height: 1.5; }

    /* ── Outlook boxes ── */
    .outlook-box {
        background: #080c14;
        border: 1px solid #1a2540;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-top: 0.8rem;
    }
    .outlook-box .outlook-label {
        font-size: 0.72rem;
        color: #6b7a99;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .outlook-box .outlook-sentiment {
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }
    .outlook-box .outlook-range {
        font-size: 0.92rem;
        color: #c0cfe8;
        margin-bottom: 0.2rem;
    }
    .outlook-box .outlook-conf {
        font-size: 0.8rem;
        color: #6b7a99;
        margin-bottom: 0.4rem;
    }

    /* ── Pattern cards ── */
    .pattern-box {
        background: #080c14;
        border: 1px solid #1a2540;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    .pattern-name { font-weight: 700; font-size: 0.9rem; }

    /* ── TF cards ── */
    .tf-card {
        background: #080c14;
        border: 1px solid #1a2540;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        display: grid;
        grid-template-columns: 48px 1fr auto auto auto;
        align-items: center;
        gap: 0.6rem;
    }
    .tf-label {
        font-weight: 800;
        color: #c0cfe8;
        font-size: 0.9rem;
    }
    .tf-scores { display: flex; gap: 0.4rem; align-items: center; font-size: 0.82rem; }

    /* ── Disclaimer ── */
    .disclaimer-box {
        background: rgba(255,152,0,0.07);
        border: 1px solid rgba(255,152,0,0.25);
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-top: 1.5rem;
        color: #c8975a;
        font-size: 0.85rem;
        line-height: 1.6;
    }

    /* ── Divider ── */
    .hr { border: none; border-top: 1px solid #1a2540; margin: 1.2rem 0; }

    /* ── Compare tab ── */
    .cmp-vs-banner {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 1rem;
        align-items: center;
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 16px;
        padding: 1.3rem 1.8rem;
        margin-bottom: 1.4rem;
    }
    .cmp-coin-block { display: flex; flex-direction: column; gap: 0.3rem; }
    .cmp-coin-block.right { align-items: flex-end; }
    .cmp-coin-name { font-size: 1.3rem; font-weight: 800; }
    .cmp-coin-sub  { font-size: 0.8rem; color: #6b7a99; font-weight: 500; }
    .cmp-vs-circle {
        width: 48px; height: 48px;
        background: #1a2540;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 0.85rem; color: #6b7a99;
        flex-shrink: 0;
    }

    .cmp-row {
        display: grid;
        grid-template-columns: 1fr 160px 1fr;
        gap: 0.5rem;
        align-items: center;
        background: #080c14;
        border: 1px solid #1a2540;
        border-radius: 10px;
        padding: 0.75rem 1.1rem;
        margin-top: 0.4rem;
        transition: border-color 0.15s;
    }
    .cmp-row:hover { border-color: #2a4080; }
    .cmp-val-a {
        text-align: left;
        font-weight: 700;
        font-size: 0.95rem;
        color: #40c4ff;
    }
    .cmp-val-b {
        text-align: right;
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffd54f;
    }
    .cmp-metric-label {
        text-align: center;
        font-size: 0.75rem;
        color: #6b7a99;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    .cmp-win  { color: #00e676 !important; }
    .cmp-lose { color: #ff5252 !important; }
    .cmp-tie  { color: #ffb74d !important; }

    .cmp-section-head {
        display: grid;
        grid-template-columns: 1fr 160px 1fr;
        gap: 0.5rem;
        padding: 0.5rem 1.1rem;
        margin-top: 1.2rem;
        margin-bottom: 0.2rem;
    }
    .cmp-head-a { text-align: left;  font-size: 0.78rem; font-weight: 700; color: #40c4ff; letter-spacing: 0.4px; text-transform: uppercase; }
    .cmp-head-b { text-align: right; font-size: 0.78rem; font-weight: 700; color: #ffd54f; letter-spacing: 0.4px; text-transform: uppercase; }
    .cmp-head-mid { text-align: center; }

    .verdict-box {
        background: linear-gradient(135deg, #0d1a35 0%, #080c14 100%);
        border: 1px solid #1a2540;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin-top: 1.5rem;
        text-align: center;
    }
    .verdict-eyebrow { font-size: 0.72rem; color: #6b7a99; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.6rem; }
    .verdict-winner  { font-size: 2rem; font-weight: 900; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
    .verdict-sub     { font-size: 0.92rem; color: #6b7a99; line-height: 1.5; }

    .bar-row { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem; }
    .bar-label { font-size: 0.8rem; font-weight: 700; min-width: 42px; }
    .bar-track { flex: 1; height: 8px; background: #1a2540; border-radius: 4px; overflow: hidden; }
    .bar-fill-a { height: 100%; background: linear-gradient(90deg,#1a6bff,#40c4ff); border-radius: 4px; }
    .bar-fill-b { height: 100%; background: linear-gradient(90deg,#d4a000,#ffd54f); border-radius: 4px; }
    .bar-val { font-size: 0.85rem; font-weight: 700; min-width: 30px; text-align: right; }

    .cmp-badge-a {
        display: inline-block; padding: 0.35rem 1rem;
        border-radius: 999px; font-weight: 700; font-size: 0.85rem;
        background: rgba(64,196,255,0.12); color: #40c4ff;
        border: 1px solid rgba(64,196,255,0.25);
    }
    .cmp-badge-b {
        display: inline-block; padding: 0.35rem 1rem;
        border-radius: 999px; font-weight: 700; font-size: 0.85rem;
        background: rgba(255,213,79,0.12); color: #ffd54f;
        border: 1px solid rgba(255,213,79,0.25);
    }

    /* ── Top Performers ── */
    .top-perf-wrap {
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 16px;
        padding: 1.1rem 1.4rem 1.2rem;
        margin-bottom: 1.4rem;
    }
    .top-perf-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .top-perf-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #6b7a99;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }
    .top-perf-tf-pills {
        display: flex;
        gap: 0.4rem;
    }
    .tf-pill {
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
        border: 1px solid #1a2540;
        color: #6b7a99;
        background: transparent;
        letter-spacing: 0.3px;
    }
    .tf-pill.active {
        background: rgba(26,107,255,0.15);
        border-color: rgba(26,107,255,0.4);
        color: #40c4ff;
    }
    .perf-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.65rem;
    }
    .perf-card {
        background: #080c14;
        border: 1px solid #1a2540;
        border-radius: 12px;
        padding: 0.85rem 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        transition: border-color 0.15s, transform 0.1s;
        position: relative;
        overflow: hidden;
    }
    .perf-card:hover { border-color: #2a4080; transform: translateY(-2px); }
    .perf-card-rank {
        position: absolute;
        top: 0.5rem; right: 0.6rem;
        font-size: 0.65rem;
        color: #1a2540;
        font-weight: 800;
    }
    .perf-card-sym  { font-size: 0.95rem; font-weight: 800; color: #ffffff; }
    .perf-card-name { font-size: 0.72rem; color: #6b7a99; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .perf-card-price{ font-size: 0.82rem; color: #c0cfe8; margin-top: 0.1rem; }
    .perf-card-pct  { font-size: 1.05rem; font-weight: 800; }
    .perf-card-pct.pos { color: #00e676; }
    .perf-card-pct.neg { color: #ff5252; }
    .perf-card-bar {
        height: 3px;
        border-radius: 2px;
        margin-top: 0.3rem;
    }
    .perf-card-bar.pos { background: linear-gradient(90deg, #00c853, #00e676); }
    .perf-card-bar.neg { background: linear-gradient(90deg, #c62828, #ff5252); }



    /* ── Top Gainers ── */
    .gainers-row { display:grid; grid-template-columns:repeat(3,1fr); gap:0.75rem; margin-bottom:1.2rem; }
    .gainer-card {
        background: #0d1117; border: 1px solid #1a2540; border-radius: 16px;
        padding: 1.1rem 1.3rem; display: flex; align-items: center; gap: 1rem;
        position: relative; overflow: hidden; transition: border-color 0.15s, transform 0.12s;
    }
    .gainer-card:hover { border-color: #00c853; transform: translateY(-2px); }
    .gainer-card::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #00c853, #00e676); border-radius: 16px 16px 0 0;
    }
    .gainer-rank { font-size:1.6rem; font-weight:900; color:#1a2540; min-width:28px; text-align:center; line-height:1; }
    .gainer-rank.r1 { color: #ffd700; }
    .gainer-rank.r2 { color: #c0c0c0; }
    .gainer-rank.r3 { color: #cd7f32; }
    .gainer-body { flex:1; min-width:0; }
    .gainer-sym  { font-size:1.05rem; font-weight:800; color:#ffffff; letter-spacing:-0.2px; }
    .gainer-name { font-size:0.75rem; color:#6b7a99; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:0.1rem; }
    .gainer-right { text-align:right; }
    .gainer-pct  { font-size:1.35rem; font-weight:900; color:#00e676; letter-spacing:-0.3px; line-height:1.1; }
    .gainer-price { font-size:0.8rem; color:#6b7a99; margin-top:0.15rem; }
    .gainers-label { font-size:0.72rem; font-weight:700; color:#6b7a99; letter-spacing:0.8px; text-transform:uppercase; margin-bottom:0.55rem; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080c14; }
    ::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }

    /* ── DCA Tab ── */
    .dca-stat-card {
        background: #0d1117;
        border: 1px solid #1a2540;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .dca-stat-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 14px 14px 0 0;
    }
    .dca-stat-card.green::before { background: linear-gradient(90deg,#00c853,#00e676); }
    .dca-stat-card.blue::before  { background: linear-gradient(90deg,#1a6bff,#40c4ff); }
    .dca-stat-card.purple::before{ background: linear-gradient(90deg,#7c4dff,#b388ff); }
    .dca-stat-card.gold::before  { background: linear-gradient(90deg,#d4a000,#ffd54f); }
    .dca-stat-card.red::before   { background: linear-gradient(90deg,#c62828,#ff5252); }
    .dca-stat-label { font-size: 0.72rem; color: #6b7a99; font-weight: 600; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .dca-stat-value { font-size: 1.55rem; font-weight: 800; color: #ffffff; letter-spacing: -0.3px; }
    .dca-stat-sub   { font-size: 0.8rem; color: #6b7a99; margin-top: 0.2rem; }
    .dca-insight {
        background: #080c14;
        border: 1px solid #1a2540;
        border-left: 3px solid #1a6bff;
        border-radius: 0 10px 10px 0;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.88rem;
        line-height: 1.6;
        color: #c0cfe8;
    }
    .dca-insight.green { border-left-color: #00c853; }
    .dca-insight.red   { border-left-color: #ff5252; }
    .dca-insight.gold  { border-left-color: #ffd54f; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Curated coin list
# -----------------------------
DEFAULT_COINS = {
    "BTC  — Bitcoin":           {"name": "Bitcoin",           "id": "bitcoin"},
    "ETH  — Ethereum":          {"name": "Ethereum",          "id": "ethereum"},
    "BNB  — BNB":               {"name": "BNB",               "id": "binancecoin"},
    "SOL  — Solana":            {"name": "Solana",            "id": "solana"},
    "XRP  — XRP":               {"name": "XRP",               "id": "ripple"},
    "ADA  — Cardano":           {"name": "Cardano",           "id": "cardano"},
    "AVAX — Avalanche":         {"name": "Avalanche",         "id": "avalanche-2"},
    "DOGE — Dogecoin":          {"name": "Dogecoin",          "id": "dogecoin"},
    "DOT  — Polkadot":          {"name": "Polkadot",          "id": "polkadot"},
    "LINK — Chainlink":         {"name": "Chainlink",         "id": "chainlink"},
    "LTC  — Litecoin":          {"name": "Litecoin",          "id": "litecoin"},
    "MATIC — Polygon":          {"name": "Polygon",           "id": "matic-network"},
    "SHIB — Shiba Inu":         {"name": "Shiba Inu",         "id": "shiba-inu"},
    "UNI  — Uniswap":           {"name": "Uniswap",           "id": "uniswap"},
    "ATOM — Cosmos":            {"name": "Cosmos",            "id": "cosmos"},
    "XLM  — Stellar":           {"name": "Stellar",           "id": "stellar"},
    "TON  — Toncoin":           {"name": "Toncoin",           "id": "the-open-network"},
    "TRX  — TRON":              {"name": "TRON",              "id": "tron"},
    "ICP  — Internet Computer": {"name": "Internet Computer", "id": "internet-computer"},
    "OP   — Optimism":          {"name": "Optimism",          "id": "optimism"},
    "ARB  — Arbitrum":          {"name": "Arbitrum",          "id": "arbitrum"},
    "FIL  — Filecoin":          {"name": "Filecoin",          "id": "filecoin"},
    "NEAR — NEAR Protocol":     {"name": "NEAR Protocol",     "id": "near"},
    "APT  — Aptos":             {"name": "Aptos",             "id": "aptos"},
    "SNEK — SNEK":              {"name": "SNEK",              "id": "snek"},
}

SHORT_TIMEFRAMES  = [1, 7, 14]
MEDIUM_TIMEFRAMES = [30, 90, 180]
ALL_TIMEFRAMES    = SHORT_TIMEFRAMES + MEDIUM_TIMEFRAMES

# -----------------------------
# Helpers
# -----------------------------
def sentiment_class(text):
    t = str(text).lower()
    if "bull" in t: return "signal-bull"
    if "bear" in t: return "signal-bear"
    return "signal-neutral"

def recommendation_class(text):
    t = str(text).lower()
    if "buy"  in t: return "rec-buy"
    if "sell" in t: return "rec-sell"
    return "rec-wait"

def confidence_label(score_diff_abs):
    if score_diff_abs >= 40: return "Very High"
    if score_diff_abs >= 28: return "High"
    if score_diff_abs >= 15: return "Medium"
    return "Low"

def clamp_price(v): return max(v, 0.0)

def format_price(value):
    if value < 0.0001: return f"${value:.8f}"
    if value < 0.01:   return f"${value:.6f}"
    if value < 1:      return f"${value:.4f}"
    return f"${value:,.2f}"

def make_range_text(low, high):
    return f"{format_price(low)} — {format_price(high)}"

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data(ttl=21600)
def get_daily_data(coin_id):  # 6h — daily candles barely change
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 365, "interval": "daily"}
    r = _coingecko_get(url, params, timeout=20)
    data = r.json()
    if "prices" not in data:
        raise Exception(data.get("status", {}).get("error_message", "Missing 'prices'"))
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")
    if "total_volumes" in data:
        vol = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
        vol["timestamp"] = pd.to_datetime(vol["timestamp"], unit="ms")
        prices = prices.merge(vol, on="timestamp", how="left")
    else:
        prices["volume"] = None
    return prices.sort_values("timestamp").reset_index(drop=True)

@st.cache_data(ttl=1800)
def get_hourly_data(coin_id):  # 30 min
    """~90 days of sub-daily data — CoinGecko auto-returns hourly for days<=90."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 90}
    r = _coingecko_get(url, params, timeout=20)
    data = r.json()
    if "prices" not in data:
        raise Exception("Missing 'prices' in hourly response")
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")
    if "total_volumes" in data:
        vol = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
        vol["timestamp"] = pd.to_datetime(vol["timestamp"], unit="ms")
        prices = prices.merge(vol, on="timestamp", how="left")
    else:
        prices["volume"] = None
    return prices.sort_values("timestamp").reset_index(drop=True)

def slice_last_days(df, days):
    if df.empty: return df.copy()
    cutoff = df["timestamp"].max() - pd.Timedelta(days=days)
    return df[df["timestamp"] >= cutoff].copy().reset_index(drop=True)

def _coingecko_get(url: str, params: dict, timeout: int = 15) -> requests.Response:
    """Wrapper around requests.get that raises a clean error on 429."""
    r = requests.get(url, params=params, timeout=timeout)
    if r.status_code == 429:
        raise Exception(
            "CoinGecko rate limit reached — the free tier allows ~30 calls/min. "
            "Data will refresh automatically from cache. Wait ~60s then retry."
        )
    if r.status_code != 200:
        raise Exception(f"CoinGecko API error {r.status_code}")
    return r

# Stablecoins and wrapped tokens to exclude from top performers
_STABLE_IDS = {
    "tether","usd-coin","dai","binance-usd","trueusd","usdd","frax",
    "paxos-standard","neutrino","fei-usd","liquity-usd","alchemix-usd",
    "gemini-dollar","husd","origin-dollar","usdn","usdp",
    "first-digital-usd","ethena-usde","usual-usd","paypal-usd",
    "stasis-eurs","sperax","defichain-dusd","curve-dao-token-1",
}
_STABLE_SYMBOLS = {
    "usdt","usdc","busd","dai","tusd","usdp","usdd","frax","susd","lusd",
    "gusd","husd","usdn","ousd","usde","usd0","pyusd","eurc","eurs","musd",
}
_WRAPPED_KEYWORDS = {"wrapped","wbtc","weth","staked","liquid","bridged"}

def _is_stable_or_wrapped(coin: dict) -> bool:
    sym  = coin.get("symbol","").lower()
    name = coin.get("name","").lower()
    cid  = coin.get("id","").lower()
    if sym in _STABLE_SYMBOLS:    return True
    if cid in _STABLE_IDS:        return True
    if any(w in name for w in _WRAPPED_KEYWORDS): return True
    # Price-based heuristic: anything pegged very close to $1
    price = coin.get("current_price") or 0
    if 0.95 <= price <= 1.05:     return True
    return False

@st.cache_data(ttl=900)
def get_top_performers():  # 15 min
    """Fetch top 250 coins across 3 pages, filter stables/wrapped, return clean list."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    all_coins = []
    for page in range(1, 3):          # pages 1-2 → 200 coins (saves 1 API call)
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": page,
            "sparkline": False,
            "price_change_percentage": "1h,24h,7d,30d",
        }
        try:
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 429:
                break          # rate-limited — use whatever we have so far
            if r.status_code != 200:
                break
            batch = r.json()
            if not batch:
                break
            all_coins.extend(batch)
        except Exception:
            break

    # Filter out stablecoins and wrapped tokens
    return [c for c in all_coins if not _is_stable_or_wrapped(c)]

# -----------------------------
# Indicators
# -----------------------------
def add_indicators(prices):
    p = prices.copy()
    n = len(p)

    # Moving averages with min_periods so short slices produce values
    p["SMA_7"]   = p["price"].rolling(window=min(7,  n), min_periods=2).mean()
    p["SMA_30"]  = p["price"].rolling(window=min(30, n), min_periods=2).mean()
    p["EMA_20"]  = p["price"].ewm(span=min(20,  n), adjust=False).mean()
    p["EMA_50"]  = p["price"].ewm(span=min(50,  n), adjust=False).mean()
    p["EMA_200"] = p["price"].ewm(span=min(200, n), adjust=False).mean()

    # Bollinger Bands
    bb_w = min(20, n)
    p["BB_MID"]   = p["price"].rolling(window=bb_w, min_periods=2).mean()
    p["STD_20"]   = p["price"].rolling(window=bb_w, min_periods=2).std()
    p["BB_UPPER"] = p["BB_MID"] + 2 * p["STD_20"]
    p["BB_LOWER"] = p["BB_MID"] - 2 * p["STD_20"]

    # RSI-14
    delta    = p["price"].diff()
    gain     = delta.where(delta > 0, 0.0)
    loss     = (-delta).where(delta < 0, 0.0)
    rsi_w    = min(14, n)
    avg_gain = gain.rolling(window=rsi_w, min_periods=2).mean()
    avg_loss = loss.rolling(window=rsi_w, min_periods=2).mean()
    rs       = avg_gain / avg_loss.replace(0, np.nan)
    p["RSI_14"] = 100 - (100 / (1 + rs))

    # Stochastic RSI
    p["STOCH_RSI_K"] = np.nan
    p["STOCH_RSI_D"] = np.nan
    if n >= 3:
        stoch_w = min(14, n)
        rsi_min = p["RSI_14"].rolling(window=stoch_w, min_periods=2).min()
        rsi_max = p["RSI_14"].rolling(window=stoch_w, min_periods=2).max()
        denom   = (rsi_max - rsi_min).replace(0, np.nan)
        p["STOCH_RSI_K"] = (p["RSI_14"] - rsi_min) / denom * 100
        p["STOCH_RSI_D"] = p["STOCH_RSI_K"].rolling(window=3, min_periods=2).mean()

    # MACD
    p["MACD"]        = (p["price"].ewm(span=min(12, n), adjust=False).mean()
                      - p["price"].ewm(span=min(26, n), adjust=False).mean())
    p["MACD_signal"] = p["MACD"].ewm(span=min(9, n), adjust=False).mean()
    p["MACD_hist"]   = p["MACD"] - p["MACD_signal"]

    # ATR (using absolute price changes as OHLC proxy)
    atr_w    = min(14, n)
    p["ATR"] = p["price"].diff().abs().rolling(window=atr_w, min_periods=2).mean()

    # OBV
    if "volume" in p.columns and p["volume"].notna().any():
        direction = np.sign(p["price"].diff().fillna(0))
        p["OBV"]     = (direction * p["volume"].fillna(0)).cumsum()
        p["OBV_EMA"] = p["OBV"].ewm(span=min(20, n), adjust=False).mean()
    else:
        p["OBV"]     = np.nan
        p["OBV_EMA"] = np.nan

    # Support / Resistance
    sr_w = min(20, n)
    p["Support_20"]    = p["price"].rolling(window=sr_w, min_periods=2).min()
    p["Resistance_20"] = p["price"].rolling(window=sr_w, min_periods=2).max()

    # Returns & volatility
    p["Returns"]       = p["price"].pct_change()
    p["Volatility_20"] = p["Returns"].rolling(window=min(20, n), min_periods=2).std()

    return p

# -----------------------------
# Pattern detection
# -----------------------------
def detect_patterns(prices):
    patterns = []
    if len(prices) < 5:
        return patterns

    close = prices["price"].values
    ret   = prices["Returns"].fillna(0).values

    # Golden / Death cross
    sma7  = prices["SMA_7"].values
    sma30 = prices["SMA_30"].values
    if all(pd.notna(v) for v in [sma7[-1], sma30[-1], sma7[-2], sma30[-2]]):
        if sma7[-2] < sma30[-2] and sma7[-1] > sma30[-1]:
            patterns.append(("🟢 Golden Cross", "SMA 7 crossed above SMA 30 — classic bullish signal.", "bull"))
        elif sma7[-2] > sma30[-2] and sma7[-1] < sma30[-1]:
            patterns.append(("🔴 Death Cross", "SMA 7 crossed below SMA 30 — classic bearish signal.", "bear"))

    # MACD crossover
    macd = prices["MACD"].values
    msig = prices["MACD_signal"].values
    if all(pd.notna(v) for v in [macd[-1], msig[-1], macd[-2], msig[-2]]):
        if macd[-2] < msig[-2] and macd[-1] > msig[-1]:
            patterns.append(("🟢 MACD Bullish Crossover", "MACD crossed above signal — upward momentum shift.", "bull"))
        elif macd[-2] > msig[-2] and macd[-1] < msig[-1]:
            patterns.append(("🔴 MACD Bearish Crossover", "MACD crossed below signal — downward momentum shift.", "bear"))

    # Bollinger Band breakout / squeeze
    bb_u = prices["BB_UPPER"].values
    bb_l = prices["BB_LOWER"].values
    bb_m = prices["BB_MID"].values
    if pd.notna(bb_u[-1]) and pd.notna(bb_l[-1]) and bb_m[-1] != 0:
        width_now  = (bb_u[-1] - bb_l[-1]) / bb_m[-1]
        width_prev = (bb_u[-5] - bb_l[-5]) / bb_m[-5] if len(prices) >= 5 and bb_m[-5] != 0 else width_now
        if width_now < width_prev * 0.70:
            patterns.append(("🟡 Bollinger Squeeze", "Bands contracting — a large move may be building.", "neutral"))
        if close[-1] > bb_u[-1]:
            patterns.append(("🔴 BB Upper Breakout", "Price above upper band — potentially overextended.", "bear"))
        elif close[-1] < bb_l[-1]:
            patterns.append(("🟢 BB Lower Bounce Zone", "Price below lower band — oversold / bounce potential.", "bull"))

    # RSI divergence (10-bar window)
    rsi = prices["RSI_14"].values
    if len(prices) >= 10 and pd.notna(rsi[-1]) and pd.notna(rsi[-10]):
        if close[-1] > close[-10] and rsi[-1] < rsi[-10]:
            patterns.append(("🔴 Bearish RSI Divergence", "Price higher but RSI lower — hidden weakness, watch for reversal.", "bear"))
        elif close[-1] < close[-10] and rsi[-1] > rsi[-10]:
            patterns.append(("🟢 Bullish RSI Divergence", "Price lower but RSI higher — hidden strength, potential bounce.", "bull"))

    # Stochastic RSI extremes
    if "STOCH_RSI_K" in prices.columns:
        sk = prices["STOCH_RSI_K"].values
        if pd.notna(sk[-1]):
            if sk[-1] > 80:
                patterns.append(("🔴 Stoch RSI Overbought", f"Stoch RSI at {sk[-1]:.0f} — short-term momentum exhaustion risk.", "bear"))
            elif sk[-1] < 20:
                patterns.append(("🟢 Stoch RSI Oversold", f"Stoch RSI at {sk[-1]:.0f} — potential short-term bounce.", "bull"))

    # 3-bar consecutive momentum
    if len(ret) >= 3:
        last3 = ret[-3:]
        if all(r > 0.005 for r in last3):
            patterns.append(("🟢 3-Bar Bullish Run", "Three consecutive up periods — strong buying pressure.", "bull"))
        elif all(r < -0.005 for r in last3):
            patterns.append(("🔴 3-Bar Bearish Run", "Three consecutive down periods — sustained selling pressure.", "bear"))

    # OBV confirmation / divergence
    obv = prices["OBV"].values if "OBV" in prices.columns else None
    if obv is not None and len(obv) >= 10 and pd.notna(obv[-1]) and pd.notna(obv[-10]):
        price_up = close[-1] > close[-10]
        obv_up   = obv[-1]  > obv[-10]
        if price_up and not obv_up:
            patterns.append(("🔴 OBV Bearish Divergence", "Price rising but OBV falling — rally lacks volume support.", "bear"))
        elif not price_up and obv_up:
            patterns.append(("🟢 OBV Bullish Divergence", "Price falling but OBV rising — selling pressure decreasing.", "bull"))

    return patterns

# -----------------------------
# Analysis engine
# -----------------------------
def analyze_prices(prices):
    latest = prices.iloc[-1]
    first  = prices.iloc[0]

    price      = latest["price"]
    rsi        = latest["RSI_14"]
    sma30      = latest["SMA_30"]
    ema20      = latest["EMA_20"]
    ema50      = latest["EMA_50"]
    macd       = latest["MACD"]
    macd_sig   = latest["MACD_signal"]
    macd_hist  = latest["MACD_hist"]
    support    = latest["Support_20"]
    resistance = latest["Resistance_20"]
    volatility = latest["Volatility_20"]
    atr        = latest["ATR"]
    bb_upper   = latest["BB_UPPER"]
    bb_lower   = latest["BB_LOWER"]
    latest_time= latest["timestamp"]
    volume     = latest.get("volume", None)
    stoch_k    = latest["STOCH_RSI_K"] if "STOCH_RSI_K" in latest.index else np.nan
    obv        = latest["OBV"]         if "OBV"         in latest.index else np.nan
    obv_ema    = latest["OBV_EMA"]     if "OBV_EMA"     in latest.index else np.nan

    pct_change = ((price - first["price"]) / first["price"]) * 100 if first["price"] != 0 else 0

    interpretation = []
    bull_score = 0
    bear_score = 0

    # SMA trend
    if pd.notna(sma30):
        if price > sma30:
            trend_text = "Bullish medium-term trend"
            interpretation.append("Price above SMA 30 — medium-term trend is bullish.")
            bull_score += 15
        else:
            trend_text = "Bearish medium-term trend"
            interpretation.append("Price below SMA 30 — medium-term trend is bearish.")
            bear_score += 15
    else:
        trend_text = "Neutral / insufficient SMA data"
        interpretation.append("Not enough data for SMA 30 analysis.")

    # EMA structure
    if pd.notna(ema20) and pd.notna(ema50):
        if ema20 > ema50:
            ema_text = "Bullish EMA structure"
            interpretation.append("EMA 20 > EMA 50 — short-term trend is bullish.")
            bull_score += 15
        else:
            ema_text = "Bearish EMA structure"
            interpretation.append("EMA 20 < EMA 50 — short-term trend is bearish.")
            bear_score += 15
    else:
        ema_text = "Neutral / insufficient EMA data"
        interpretation.append("Not enough data for EMA analysis.")

    # RSI
    if pd.notna(rsi):
        if 50 <= rsi <= 70:
            rsi_text = "Bullish RSI"
            interpretation.append(f"RSI {rsi:.1f} — constructive bullish zone.")
            bull_score += 12
        elif rsi > 70:
            rsi_text = "Overbought RSI"
            interpretation.append(f"RSI {rsi:.1f} — overbought, caution on new longs.")
            bear_score += 10
        elif 30 <= rsi < 50:
            rsi_text = "Weak RSI"
            interpretation.append(f"RSI {rsi:.1f} — momentum is weak.")
            bear_score += 10
        elif rsi < 30:
            rsi_text = "Oversold RSI — rebound possible"
            interpretation.append(f"RSI {rsi:.1f} — oversold, watch for a bounce.")
            bull_score += 8
        else:
            rsi_text = "Neutral RSI"
            interpretation.append(f"RSI {rsi:.1f} — neutral zone.")
    else:
        rsi_text = "RSI unavailable"
        interpretation.append("Insufficient data for RSI.")

    # Stochastic RSI
    if pd.notna(stoch_k):
        if stoch_k > 80:
            interpretation.append(f"Stoch RSI {stoch_k:.0f} — short-term overbought.")
            bear_score += 8
        elif stoch_k < 20:
            interpretation.append(f"Stoch RSI {stoch_k:.0f} — short-term oversold, bounce likely.")
            bull_score += 8
        else:
            bull_score += 5 if stoch_k > 50 else 0
            bear_score += 5 if stoch_k <= 50 else 0

    # MACD
    if pd.notna(macd) and pd.notna(macd_sig):
        if macd > macd_sig:
            macd_text = "Bullish momentum (MACD)"
            interpretation.append("MACD above signal line — bullish momentum.")
            bull_score += 12
        else:
            macd_text = "Bearish momentum (MACD)"
            interpretation.append("MACD below signal line — bearish momentum.")
            bear_score += 12
        # Histogram acceleration
        if pd.notna(macd_hist) and len(prices) > 2:
            prev_hist = prices["MACD_hist"].iloc[-2]
            if pd.notna(prev_hist):
                if macd_hist > prev_hist and macd_hist > 0:
                    interpretation.append("MACD histogram expanding bullishly — acceleration.")
                    bull_score += 5
                elif macd_hist < prev_hist and macd_hist < 0:
                    interpretation.append("MACD histogram expanding bearishly — acceleration.")
                    bear_score += 5
    else:
        macd_text = "MACD unavailable"
        interpretation.append("Insufficient data for MACD.")

    # Bollinger Bands position
    if pd.notna(bb_upper) and pd.notna(bb_lower) and (bb_upper - bb_lower) > 0:
        bb_pos = (price - bb_lower) / (bb_upper - bb_lower)
        if bb_pos > 0.85:
            interpretation.append("Price near upper Bollinger Band — potential resistance / mean reversion.")
            bear_score += 7
        elif bb_pos < 0.15:
            interpretation.append("Price near lower Bollinger Band — potential support / bounce.")
            bull_score += 7

    # OBV trend
    if pd.notna(obv) and pd.notna(obv_ema):
        if obv > obv_ema:
            interpretation.append("OBV above its EMA — volume confirms the uptrend.")
            bull_score += 8
        else:
            interpretation.append("OBV below its EMA — volume pressure is bearish.")
            bear_score += 8

    # Support / Resistance proximity
    if pd.notna(support) and pd.notna(resistance) and resistance > support:
        r_size = resistance - support
        if (price - support) / r_size <= 0.20:
            interpretation.append("Trading near recent support — potential bounce zone.")
            bull_score += 8
        if (resistance - price) / r_size <= 0.20:
            interpretation.append("Trading near recent resistance — potential ceiling.")
            bear_score += 8

    # ATR volatility context
    atr_pct = (atr / price * 100) if (pd.notna(atr) and price > 0) else 0
    if atr_pct > 5:
        volatility_label = f"High volatility (ATR {atr_pct:.1f}% of price)"
    elif atr_pct > 2:
        volatility_label = f"Moderate volatility (ATR {atr_pct:.1f}% of price)"
    else:
        volatility_label = f"Low volatility (ATR {atr_pct:.1f}% of price)"

    # Pattern detection (adds to scores)
    patterns       = detect_patterns(prices)
    pattern_bull   = sum(1 for _, _, s in patterns if s == "bull")
    pattern_bear   = sum(1 for _, _, s in patterns if s == "bear")

    bull_score = min(bull_score + pattern_bull * 4, 100)
    bear_score = min(bear_score + pattern_bear * 4, 100)
    score_diff     = bull_score - bear_score
    score_diff_abs = abs(score_diff)

    # Recommendation
    if score_diff >= 35:
        recommendation = "STRONG BUY BIAS"
        scenario = ("Multiple indicators strongly align bullishly. Trend, momentum, and volume "
                    "support upside continuation. Risk management is still essential.")
    elif score_diff >= 15:
        recommendation = "BUY BIAS"
        scenario = ("Bullish signals outweigh bearish ones. Momentum and trend lean upward, "
                    "but confirmation before entering positions is advisable.")
    elif score_diff <= -35:
        recommendation = "STRONG SELL BIAS"
        scenario = ("Strong bearish alignment across indicators. Trend, momentum, and volume "
                    "all point to downside risk. Protect capital carefully.")
    elif score_diff <= -15:
        recommendation = "SELL BIAS"
        scenario = ("More bearish signals than bullish. Momentum is weighted to the downside, "
                    "though reversals remain possible on any positive catalyst.")
    else:
        recommendation = "HOLD / MIXED"
        scenario = ("Signals are mixed without a clear directional edge. "
                    "Waiting for a breakout or cleaner setup is advisable.")

    # ATR-based asymmetric price targets
    if pd.isna(volatility): volatility = 0.03
    if pd.isna(atr):        atr        = price * 0.02

    bias = float(np.clip(score_diff / 50, -1, 1))

    def atr_range(mult):
        base     = atr * mult
        upside   = base * (1 + bias * 0.5)
        downside = base * (1 - bias * 0.5)
        return make_range_text(clamp_price(price - downside), price + upside)

    st_label  = "Bullish" if score_diff >= 15 else ("Bearish" if score_diff <= -15 else "Neutral")
    mt_label  = st_label
    lt_label  = st_label

    short_term_outlook = {
        "label": st_label,
        "range": atr_range(1.5),
        "confidence": confidence_label(score_diff_abs),
        "text": (f"ATR-based short-term range ({atr_pct:.1f}% volatility). "
                 + ("Momentum leans bullish." if score_diff >= 15
                    else "Momentum leans bearish." if score_diff <= -15
                    else "No clear short-term direction.")),
    }

    if pd.notna(support) and pd.notna(resistance) and resistance > support:
        mt_low  = min(support  * 0.98, price - atr * 3.5 * (1 - bias * 0.4))
        mt_high = max(resistance * 1.02, price + atr * 3.5 * (1 + bias * 0.4))
    else:
        mt_low  = clamp_price(price - atr * 3.5 * (1 - bias * 0.4))
        mt_high = price + atr * 3.5 * (1 + bias * 0.4)

    medium_term_outlook = {
        "label": mt_label,
        "range": make_range_text(clamp_price(mt_low), mt_high),
        "confidence": confidence_label(score_diff_abs),
        "text": ("Support/Resistance levels factored in. "
                 + ("Structure remains constructive." if score_diff >= 15
                    else "Downside continuation possible." if score_diff <= -15
                    else "No dominant medium-term direction.")),
    }

    long_term_outlook = {
        "label": lt_label,
        "range": atr_range(7.0),
        "confidence": "Low" if score_diff_abs < 35 else "Medium",
        "text": "Long-term ranges are wide — treat as scenario planning, not precise targets.",
    }

    return {
        "price": price, "rsi": rsi, "pct_change": pct_change,
        "latest_time": latest_time, "volume": volume,
        "support": support, "resistance": resistance,
        "atr": atr, "atr_pct": atr_pct, "volatility_label": volatility_label,
        "stoch_k": stoch_k,
        "trend_text": trend_text, "ema_text": ema_text,
        "rsi_text": rsi_text, "macd_text": macd_text,
        "interpretation": interpretation,
        "recommendation": recommendation, "scenario": scenario,
        "bull_score": bull_score, "bear_score": bear_score,
        "score_diff": score_diff, "score_diff_abs": score_diff_abs,
        "short_term_outlook": short_term_outlook,
        "medium_term_outlook": medium_term_outlook,
        "long_term_outlook": long_term_outlook,
        "patterns": patterns,
    }

# -----------------------------
# Chart panels
# -----------------------------
def build_figure(prices, coin_label, days, recommendation, support, resistance):
    """Build a fully interactive Plotly chart with 4 linked sub-panels."""

    BG        = "#080c14"
    PANEL_BG  = "#0d1117"
    GRID      = "rgba(255,255,255,0.06)"
    FONT_COL  = "#c0cfe8"
    LABEL_COL = "#6b7a99"

    has_volume = "volume" in prices.columns and prices["volume"].notna().any()
    has_obv    = "OBV"    in prices.columns and prices["OBV"].notna().any()

    row_heights = [0.50, 0.18, 0.18, 0.14]
    subplot_titles = [
        f"{coin_label} — Last {days}d",
        "RSI 14 + Stoch RSI",
        "MACD",
        "Volume" + (" + OBV" if has_obv else ""),
    ]

    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
        subplot_titles=subplot_titles,
    )

    ts = prices["timestamp"]

    # ── Panel 1: Price + MAs + Bollinger Bands ────────────────────────────
    # BB fill
    fig.add_trace(go.Scatter(
        x=ts, y=prices["BB_UPPER"],
        line=dict(color="rgba(139,148,243,0)"), showlegend=False,
        hoverinfo="skip", name="BB Upper",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ts, y=prices["BB_LOWER"],
        fill="tonexty", fillcolor="rgba(121,134,203,0.08)",
        line=dict(color="rgba(139,148,243,0)"), showlegend=False,
        hoverinfo="skip", name="BB Lower",
    ), row=1, col=1)

    # EMA 200 zone (±1% band — acts as dynamic S/R)
    if "EMA_200" in prices.columns and prices["EMA_200"].notna().any():
        ema200 = prices["EMA_200"]
        fig.add_trace(go.Scatter(
            x=ts, y=ema200 * 1.01,
            line=dict(color="rgba(0,0,0,0)"), showlegend=False,
            hoverinfo="skip", name="EMA200 Zone Top",
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=ts, y=ema200 * 0.99,
            fill="tonexty", fillcolor="rgba(179,136,255,0.10)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False,
            hoverinfo="skip", name="EMA200 Zone",
        ), row=1, col=1)

    # BB lines
    for col_name, color, dash, name in [
        ("BB_UPPER", "#8e99f3", "dot",     "BB Upper"),
        ("BB_LOWER", "#8e99f3", "dot",     "BB Lower"),
        ("EMA_200",  "#b388ff", "dashdot", "EMA 200"),
        ("SMA_7",    "#ffd54f", "dash",    "SMA 7"),
        ("SMA_30",   "#ff8a65", "dash",    "SMA 30"),
        ("EMA_20",   "#00e5ff", "dashdot", "EMA 20"),
        ("EMA_50",   "#ffb74d", "dashdot", "EMA 50"),
    ]:
        if col_name in prices.columns and prices[col_name].notna().any():
            fig.add_trace(go.Scatter(
                x=ts, y=prices[col_name],
                name=name,
                line=dict(color=color, width=1.2, dash=dash),
                hovertemplate=f"<b>{name}</b>: %{{y:.6g}}<extra></extra>",
            ), row=1, col=1)

    # Price line
    fig.add_trace(go.Scatter(
        x=ts, y=prices["price"],
        name="Price",
        line=dict(color="#40c4ff", width=2),
        hovertemplate="<b>%{x|%Y-%m-%d %H:%M}</b><br>Price: <b>%{y:.6g}</b><extra></extra>",
    ), row=1, col=1)

    # Support / Resistance
    if pd.notna(support):
        fig.add_hline(y=support, line=dict(color="#00c853", width=1.2, dash="dot"),
                      annotation_text="Support", annotation_font_color="#00c853",
                      annotation_position="right", row=1, col=1)
    if pd.notna(resistance):
        fig.add_hline(y=resistance, line=dict(color="#ff5252", width=1.2, dash="dot"),
                      annotation_text="Resistance", annotation_font_color="#ff5252",
                      annotation_position="right", row=1, col=1)

    # Recommendation badge (annotation top-right)
    rec_color = "#00c853" if "BUY" in recommendation else "#ff5252" if "SELL" in recommendation else "#ff9800"
    fig.add_annotation(
        xref="x domain", yref="y domain",
        x=0.99, y=0.97,
        text=f"<b>{recommendation}</b>",
        showarrow=False,
        font=dict(size=13, color=rec_color),
        bgcolor="rgba(13,17,23,0.85)",
        bordercolor=rec_color,
        borderwidth=1,
        borderpad=6,
        row=1, col=1,
    )

    # ── Panel 2: RSI + Stoch RSI ──────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts, y=prices["RSI_14"],
        name="RSI 14",
        line=dict(color="#ab47bc", width=1.8),
        hovertemplate="RSI: <b>%{y:.1f}</b><extra></extra>",
    ), row=2, col=1)

    if "STOCH_RSI_K" in prices.columns and prices["STOCH_RSI_K"].notna().any():
        fig.add_trace(go.Scatter(
            x=ts, y=prices["STOCH_RSI_K"],
            name="Stoch K",
            line=dict(color="#f48fb1", width=1.0),
            opacity=0.75,
            hovertemplate="Stoch K: <b>%{y:.0f}</b><extra></extra>",
        ), row=2, col=1)
    if "STOCH_RSI_D" in prices.columns and prices["STOCH_RSI_D"].notna().any():
        fig.add_trace(go.Scatter(
            x=ts, y=prices["STOCH_RSI_D"],
            name="Stoch D",
            line=dict(color="#f8bbd0", width=1.0, dash="dot"),
            opacity=0.6,
            hovertemplate="Stoch D: <b>%{y:.0f}</b><extra></extra>",
        ), row=2, col=1)

    for level, color in [(70, "#ff5252"), (30, "#00c853")]:
        fig.add_hline(y=level, line=dict(color=color, width=0.8, dash="dash"), row=2, col=1)

    # ── Panel 3: MACD ─────────────────────────────────────────────────────
    if "MACD" in prices.columns:
        fig.add_trace(go.Scatter(
            x=ts, y=prices["MACD"],
            name="MACD",
            line=dict(color="#40c4ff", width=1.8),
            hovertemplate="MACD: <b>%{y:.6g}</b><extra></extra>",
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=ts, y=prices["MACD_signal"],
            name="Signal",
            line=dict(color="#ffd54f", width=1.4),
            hovertemplate="Signal: <b>%{y:.6g}</b><extra></extra>",
        ), row=3, col=1)
        hist_colors = ["#00c853" if v >= 0 else "#ff5252"
                       for v in prices["MACD_hist"].fillna(0)]
        fig.add_trace(go.Bar(
            x=ts, y=prices["MACD_hist"],
            name="Histogram",
            marker_color=hist_colors,
            opacity=0.55,
            hovertemplate="Hist: <b>%{y:.6g}</b><extra></extra>",
        ), row=3, col=1)
        fig.add_hline(y=0, line=dict(color="rgba(255,255,255,0.3)", width=0.8), row=3, col=1)

    # ── Panel 4: Volume + OBV ─────────────────────────────────────────────
    if has_volume:
        direction  = prices["price"].diff().fillna(0)
        vol_colors = ["#00c853" if d >= 0 else "#ff5252" for d in direction]
        fig.add_trace(go.Bar(
            x=ts, y=prices["volume"],
            name="Volume",
            marker_color=vol_colors,
            opacity=0.6,
            hovertemplate="Vol: <b>%{y:,.0f}</b><extra></extra>",
        ), row=4, col=1)
        if has_obv:
            fig.add_trace(go.Scatter(
                x=ts, y=prices["OBV"],
                name="OBV",
                line=dict(color="#80cbc4", width=1.2),
                yaxis="y5",
                hovertemplate="OBV: <b>%{y:,.0f}</b><extra></extra>",
            ), row=4, col=1)
            fig.add_trace(go.Scatter(
                x=ts, y=prices["OBV_EMA"],
                name="OBV EMA",
                line=dict(color="#26a69a", width=1.0, dash="dash"),
                yaxis="y5",
                hovertemplate="OBV EMA: <b>%{y:,.0f}</b><extra></extra>",
            ), row=4, col=1)

    # ── Layout ────────────────────────────────────────────────────────────
    axis_style = dict(
        showgrid=True, gridcolor=GRID,
        zeroline=False,
        tickfont=dict(color=LABEL_COL, size=11),
        title_font=dict(color=LABEL_COL),
        linecolor="#1a2540",
    )

    fig.update_layout(
        height=820,
        paper_bgcolor=BG,
        plot_bgcolor=PANEL_BG,
        font=dict(family="Inter, sans-serif", color=FONT_COL),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#0d1117",
            bordercolor="#2a4080",
            font=dict(color="#e8ecf0", size=12),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="left",   x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=FONT_COL),
        ),
        xaxis=dict(showticklabels=False, **axis_style),
        xaxis2=dict(showticklabels=False, **axis_style),
        xaxis3=dict(showticklabels=False, **axis_style),
        xaxis4=dict(**axis_style),
        yaxis =dict(title="Price (USD)", **axis_style),
        yaxis2=dict(title="RSI", range=[0, 100], **axis_style),
        yaxis3=dict(title="MACD", **axis_style),
        yaxis4=dict(title="Volume", **axis_style),
        margin=dict(l=60, r=60, t=50, b=40),
        dragmode="pan",
    )

    # Style subplot title annotations
    for ann in fig.layout.annotations:
        ann.font.color  = LABEL_COL
        ann.font.size   = 11

    # Ensure all panels share the same background
    for i in range(1, 5):
        fig.update_xaxes(row=i, col=1, showgrid=True, gridcolor=GRID, linecolor="#1a2540")
        fig.update_yaxes(row=i, col=1, showgrid=True, gridcolor=GRID, linecolor="#1a2540",
                         zeroline=False)

    return fig


def build_compare_plotly(data_a, data_b, label_a, label_b, days):
    """Interactive Plotly comparison chart — normalised price + RSI."""
    BG       = "#080c14"
    PANEL_BG = "#0d1117"
    GRID     = "rgba(255,255,255,0.06)"

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.65, 0.35],
        subplot_titles=[f"Indexed Price Comparison — Last {days}d", "RSI 14"],
    )

    def norm(s):
        base = s.iloc[0]
        return s / base * 100 if base != 0 else s

    fig.add_trace(go.Scatter(
        x=data_a["timestamp"], y=norm(data_a["price"]),
        name=label_a, line=dict(color="#40c4ff", width=2),
        hovertemplate=f"<b>{label_a}</b>: %{{y:.2f}}<extra></extra>",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=data_b["timestamp"], y=norm(data_b["price"]),
        name=label_b, line=dict(color="#ffd54f", width=2),
        hovertemplate=f"<b>{label_b}</b>: %{{y:.2f}}<extra></extra>",
    ), row=1, col=1)
    fig.add_hline(y=100, line=dict(color="rgba(255,255,255,0.2)", dash="dash", width=1),
                  row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data_a["timestamp"], y=data_a["RSI_14"],
        name=f"RSI {label_a}", line=dict(color="#40c4ff", width=1.6),
        hovertemplate="RSI: <b>%{y:.1f}</b><extra></extra>",
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=data_b["timestamp"], y=data_b["RSI_14"],
        name=f"RSI {label_b}", line=dict(color="#ffd54f", width=1.6),
        hovertemplate="RSI: <b>%{y:.1f}</b><extra></extra>",
    ), row=2, col=1)
    for level, color in [(70, "#ff5252"), (30, "#00c853")]:
        fig.add_hline(y=level, line=dict(color=color, width=0.8, dash="dash"), row=2, col=1)

    axis_kw = dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(color="#6b7a99", size=11), linecolor="#1a2540")
    fig.update_layout(
        height=520,
        paper_bgcolor=BG, plot_bgcolor=PANEL_BG,
        font=dict(family="Inter, sans-serif", color="#c0cfe8"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#0d1117", bordercolor="#2a4080",
                        font=dict(color="#e8ecf0", size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(showticklabels=False, **axis_kw),
        xaxis2=dict(**axis_kw),
        yaxis=dict(title="Indexed (base=100)", **axis_kw),
        yaxis2=dict(title="RSI", range=[0, 100], **axis_kw),
        margin=dict(l=60, r=40, t=50, b=40),
        dragmode="pan",
    )
    for ann in fig.layout.annotations:
        ann.font.color = "#6b7a99"
        ann.font.size  = 11
    return fig


def figure_to_png_bytes(fig):
    """Keep PNG export working for the download button (uses matplotlib fallback)."""
    buf = io.BytesIO()
    # fig here may be a Plotly figure; use kaleido if available, else skip
    try:
        img_bytes = fig.to_image(format="png", width=1600, height=900, scale=2)
        buf.write(img_bytes)
    except Exception:
        buf.write(b"")
    buf.seek(0)
    return buf

# -----------------------------
# UI render helpers
# -----------------------------
def render_outlook(title, outlook):
    cc  = sentiment_class(outlook["label"])
    lbl = outlook["label"]
    st.markdown(f"""
    <div class="outlook-box">
        <div class="outlook-label">{title}</div>
        <div class="outlook-sentiment {cc}">{lbl}</div>
        <div class="outlook-range">🎯 {outlook['range']}</div>
        <div class="outlook-conf">Confidence: <strong>{outlook['confidence']}</strong></div>
        <div class="small-note">{outlook['text']}</div>
    </div>
    """, unsafe_allow_html=True)

def render_patterns(patterns):
    if not patterns:
        st.markdown('<div class="pattern-box small-note" style="padding:1rem;">No significant patterns detected in this timeframe.</div>', unsafe_allow_html=True)
        return
    for name, desc, side in patterns:
        color = "#00e676" if side == "bull" else "#ff5252" if side == "bear" else "#ffb74d"
        dot   = "🟢" if side == "bull" else "🔴" if side == "bear" else "🟡"
        st.markdown(f"""
        <div class="pattern-box">
            <div class="pattern-name" style="color:{color};">{dot} {name}</div>
            <div class="small-note" style="margin-top:0.25rem;">{desc}</div>
        </div>""", unsafe_allow_html=True)

def render_tf_row(tf_days, a):
    rec     = a["recommendation"]
    rc      = recommendation_class(rec)
    rsi_str = f"{a['rsi']:.0f}" if pd.notna(a['rsi']) else "—"
    conf    = a['short_term_outlook']['confidence']
    st.markdown(f"""
    <div class="tf-card">
        <span class="tf-label">{tf_days}d</span>
        <span class="rec-badge {rc}" style="font-size:0.72rem;padding:0.3rem 0.7rem;">{rec}</span>
        <span class="tf-scores">
            <span class="signal-bull">▲&nbsp;{a['bull_score']}</span>
            <span style="color:#1a2540;">|</span>
            <span class="signal-bear">▼&nbsp;{a['bear_score']}</span>
        </span>
        <span class="small-note">RSI&nbsp;{rsi_str}</span>
        <span class="small-note" style="color:#1a6bff;font-weight:600;">{conf}</span>
    </div>""", unsafe_allow_html=True)


# ============================
# Compare tab helpers
# ============================
COLOR_A = "#40c4ff"
COLOR_B = "#ffd54f"




def cmp_row(label, val_a, val_b, higher_is_better=True, fmt_fn=None):
    """Render a single comparison row with winner highlighting."""
    fmt = fmt_fn or (lambda v: str(v))
    try:
        a_num = float(val_a)
        b_num = float(val_b)
        if abs(a_num - b_num) < 1e-12:
            cls_a = cls_b = "cmp-tie"
        elif (a_num > b_num) == higher_is_better:
            cls_a, cls_b = "cmp-win", "cmp-lose"
        else:
            cls_a, cls_b = "cmp-lose", "cmp-win"
    except (TypeError, ValueError):
        cls_a = cls_b = ""

    st.markdown(f"""
    <div class="cmp-row">
        <div class="cmp-val-a {cls_a}">{fmt(val_a)}</div>
        <div class="cmp-metric-label">{label}</div>
        <div class="cmp-val-b {cls_b}">{fmt(val_b)}</div>
    </div>""", unsafe_allow_html=True)


def render_compare_tab():
    # ── Controls ──────────────────────────────────────────────────────────
    coin_keys = list(DEFAULT_COINS.keys())
    cc1, cc2, cc3, cc4 = st.columns([3, 3, 2, 1])
    with cc1:
        key_a = st.selectbox("Token A", coin_keys, index=0, key="cmp_a")
    with cc2:
        key_b = st.selectbox("Token B", coin_keys, index=1, key="cmp_b")
    with cc3:
        cmp_days = st.selectbox("Period (days)", [7, 14, 30, 90, 180], index=2, key="cmp_days")
    with cc4:
        st.write(""); st.write("")
        st.button("Compare", use_container_width=True, key="cmp_run")

    if key_a == key_b:
        st.warning("Please select two different tokens to compare.")
        return

    info_a  = DEFAULT_COINS[key_a]
    info_b  = DEFAULT_COINS[key_b]
    sym_a   = key_a.split("—")[0].strip().split()[0]
    sym_b   = key_b.split("—")[0].strip().split()[0]
    name_a  = info_a["name"]
    name_b  = info_b["name"]
    label_a = f"{name_a} ({sym_a})"
    label_b = f"{name_b} ({sym_b})"

    try:
        with st.spinner(f"Loading {sym_a} and {sym_b}..."):
            src_a  = get_hourly_data(info_a["id"]) if cmp_days <= 14 else get_daily_data(info_a["id"])
            src_b  = get_hourly_data(info_b["id"]) if cmp_days <= 14 else get_daily_data(info_b["id"])
            data_a = add_indicators(slice_last_days(src_a, cmp_days))
            data_b = add_indicators(slice_last_days(src_b, cmp_days))
            an_a   = analyze_prices(data_a)
            an_b   = analyze_prices(data_b)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    # ── VS banner ─────────────────────────────────────────────────────────
    pct_a     = an_a["pct_change"]
    pct_b     = an_b["pct_change"]
    pct_col_a = "#00e676" if pct_a >= 0 else "#ff5252"
    pct_col_b = "#00e676" if pct_b >= 0 else "#ff5252"
    rc_a      = recommendation_class(an_a["recommendation"])
    rc_b      = recommendation_class(an_b["recommendation"])

    st.markdown(f"""
    <div class="cmp-vs-banner">
        <div class="cmp-coin-block">
            <div class="cmp-coin-name" style="color:#40c4ff;">{sym_a}</div>
            <div class="cmp-coin-sub">{name_a}</div>
            <div style="margin-top:0.5rem;">
                <div style="font-size:1.5rem;font-weight:800;color:#ffffff;">{format_price(an_a['price'])}</div>
                <div style="font-size:0.9rem;font-weight:700;color:{pct_col_a};">{pct_a:+.2f}% ({cmp_days}d)</div>
            </div>
            <div style="margin-top:0.5rem;"><span class="rec-badge {rc_a}">{an_a['recommendation']}</span></div>
        </div>
        <div class="cmp-vs-circle">VS</div>
        <div class="cmp-coin-block right">
            <div class="cmp-coin-name" style="color:#ffd54f;">{sym_b}</div>
            <div class="cmp-coin-sub">{name_b}</div>
            <div style="margin-top:0.5rem;">
                <div style="font-size:1.5rem;font-weight:800;color:#ffffff;">{format_price(an_b['price'])}</div>
                <div style="font-size:0.9rem;font-weight:700;color:{pct_col_b};">{pct_b:+.2f}% ({cmp_days}d)</div>
            </div>
            <div style="margin-top:0.5rem;"><span class="rec-badge {rc_b}">{an_b['recommendation']}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Overlay chart ──────────────────────────────────────────────────────
    fig_cmp = build_compare_plotly(data_a, data_b, label_a, label_b, cmp_days)
    st.plotly_chart(fig_cmp, use_container_width=True, config={
        "scrollZoom": True,
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["select2d", "lasso2d"],
    })

    # ── Comparison rows helper ─────────────────────────────────────────────
    def cmp_row(label, val_a, val_b, higher_is_better=True, fmt_fn=None):
        fmt = fmt_fn or str
        try:
            a_n = float(val_a); b_n = float(val_b)
            if abs(a_n - b_n) < 1e-12:
                cls_a = cls_b = "cmp-tie"
            elif (a_n > b_n) == higher_is_better:
                cls_a, cls_b = "cmp-win", "cmp-lose"
            else:
                cls_a, cls_b = "cmp-lose", "cmp-win"
        except (TypeError, ValueError):
            cls_a = cls_b = ""
        st.markdown(f"""
        <div class="cmp-row">
            <div class="cmp-val-a {cls_a}">{fmt(val_a)}</div>
            <div class="cmp-metric-label">{label}</div>
            <div class="cmp-val-b {cls_b}">{fmt(val_b)}</div>
        </div>""", unsafe_allow_html=True)

    def safe_fmt_price(v):
        try: return format_price(float(v)) if not (isinstance(v, float) and np.isnan(v)) else "N/A"
        except: return "N/A"

    def safe_fmt_f1(v):
        try: return f"{float(v):.1f}" if not (isinstance(v, float) and np.isnan(v)) else "N/A"
        except: return "N/A"

    def safe_fmt_f0(v):
        try: return f"{float(v):.0f}" if not (isinstance(v, float) and np.isnan(v)) else "N/A"
        except: return "N/A"

    # ── Two-column comparison tables ───────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        # Column header
        st.markdown(f"""
        <div class="cmp-section-head">
            <div class="cmp-head-a">{sym_a}</div>
            <div class="cmp-head-mid"></div>
            <div class="cmp-head-b">{sym_b}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-box" style="margin-top:0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Price & Returns</div>', unsafe_allow_html=True)
        cmp_row(f"{cmp_days}d Return",    pct_a,             pct_b,             True,  lambda v: f"{float(v):+.2f}%")
        cmp_row("ATR Volatility",         an_a["atr_pct"],   an_b["atr_pct"],   False, lambda v: f"{float(v):.2f}%")
        cmp_row("Support",                an_a["support"] if pd.notna(an_a["support"]) else float("nan"),
                                          an_b["support"] if pd.notna(an_b["support"]) else float("nan"),
                                          True, safe_fmt_price)
        cmp_row("Resistance",             an_a["resistance"] if pd.notna(an_a["resistance"]) else float("nan"),
                                          an_b["resistance"] if pd.notna(an_b["resistance"]) else float("nan"),
                                          True, safe_fmt_price)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Momentum Indicators</div>', unsafe_allow_html=True)
        cmp_row("RSI 14",    an_a["rsi"]     if pd.notna(an_a["rsi"])     else float("nan"),
                             an_b["rsi"]     if pd.notna(an_b["rsi"])     else float("nan"),
                             True, safe_fmt_f1)
        cmp_row("Stoch RSI", an_a["stoch_k"] if pd.notna(an_a["stoch_k"]) else float("nan"),
                             an_b["stoch_k"] if pd.notna(an_b["stoch_k"]) else float("nan"),
                             True, safe_fmt_f0)
        cmp_row("Bull Score", an_a["bull_score"], an_b["bull_score"], True,  lambda v: f"{int(v)}/100")
        cmp_row("Bear Score", an_a["bear_score"], an_b["bear_score"], False, lambda v: f"{int(v)}/100")
        cmp_row("Net Score",  an_a["score_diff"], an_b["score_diff"], True,  lambda v: f"{int(v):+d}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-box" style="margin-top:2.85rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Signal Strength</div>', unsafe_allow_html=True)

        # Bull score bars
        st.markdown(f"""
        <div style="margin-bottom:1.2rem;">
            <div class="small-note" style="margin-bottom:0.6rem;">Bull Score</div>
            <div class="bar-row">
                <div class="bar-label" style="color:#40c4ff;">{sym_a}</div>
                <div class="bar-track"><div class="bar-fill-a" style="width:{an_a['bull_score']}%;"></div></div>
                <div class="bar-val" style="color:#40c4ff;">{an_a['bull_score']}</div>
            </div>
            <div class="bar-row">
                <div class="bar-label" style="color:#ffd54f;">{sym_b}</div>
                <div class="bar-track"><div class="bar-fill-b" style="width:{an_b['bull_score']}%;"></div></div>
                <div class="bar-val" style="color:#ffd54f;">{an_b['bull_score']}</div>
            </div>
        </div>
        <div>
            <div class="small-note" style="margin-bottom:0.6rem;">Bear Score</div>
            <div class="bar-row">
                <div class="bar-label" style="color:#40c4ff;">{sym_a}</div>
                <div class="bar-track"><div style="width:{an_a['bear_score']}%;height:100%;background:linear-gradient(90deg,#7f1414,#ff5252);border-radius:4px;"></div></div>
                <div class="bar-val" style="color:#ff5252;">{an_a['bear_score']}</div>
            </div>
            <div class="bar-row">
                <div class="bar-label" style="color:#ffd54f;">{sym_b}</div>
                <div class="bar-track"><div style="width:{an_b['bear_score']}%;height:100%;background:linear-gradient(90deg,#7f1414,#ff5252);border-radius:4px;"></div></div>
                <div class="bar-val" style="color:#ff5252;">{an_b['bear_score']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # MTF snapshot
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Signal Across Timeframes</div>', unsafe_allow_html=True)

        # Reuse already-fetched src_a / src_b — no extra API calls
        mtf_a = {}; mtf_b = {}
        for tf in [7, 30, 90]:
            s = src_a if tf <= 14 else src_a
            mtf_a[tf] = analyze_prices(add_indicators(slice_last_days(s, tf)))
            s = src_b if tf <= 14 else src_b
            mtf_b[tf] = analyze_prices(add_indicators(slice_last_days(s, tf)))

        for tf in [7, 30, 90]:
            ra = recommendation_class(mtf_a[tf]["recommendation"])
            rb = recommendation_class(mtf_b[tf]["recommendation"])
            st.markdown(f"""
            <div class="cmp-row" style="margin-top:0.4rem;">
                <div class="cmp-val-a"><span class="rec-badge {ra}" style="font-size:0.72rem;padding:0.2rem 0.6rem;">{mtf_a[tf]['recommendation']}</span></div>
                <div class="cmp-metric-label">{tf}d</div>
                <div class="cmp-val-b" style="text-align:right;"><span class="rec-badge {rb}" style="font-size:0.72rem;padding:0.2rem 0.6rem;">{mtf_b[tf]['recommendation']}</span></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Pattern comparison ─────────────────────────────────────────────────
    pat_a = an_a["patterns"]
    pat_b = an_b["patterns"]
    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{sym_a} Patterns</div>', unsafe_allow_html=True)
        if pat_a:
            for name, desc, side in pat_a:
                color = "#00e676" if side == "bull" else "#ff5252" if side == "bear" else "#ffb74d"
                st.markdown(f'<div class="pattern-box"><div class="pattern-name" style="color:{color};">{name}</div><div class="small-note" style="margin-top:0.2rem;">{desc}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="small-note" style="padding:0.5rem 0;">No patterns detected.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with pc2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{sym_b} Patterns</div>', unsafe_allow_html=True)
        if pat_b:
            for name, desc, side in pat_b:
                color = "#00e676" if side == "bull" else "#ff5252" if side == "bear" else "#ffb74d"
                st.markdown(f'<div class="pattern-box"><div class="pattern-name" style="color:{color};">{name}</div><div class="small-note" style="margin-top:0.2rem;">{desc}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="small-note" style="padding:0.5rem 0;">No patterns detected.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Verdict ───────────────────────────────────────────────────────────
    score_a = an_a["score_diff"]
    score_b = an_b["score_diff"]
    margin  = abs(score_a - score_b)

    if margin < 5:
        winner_html = "<span style='color:#ffb74d;'>🟡 Too close to call</span>"
        verdict_sub = f"Both tokens have very similar signal strength over {cmp_days} days."
    elif score_a > score_b:
        winner_html = f"<span style='color:#40c4ff;'>🏆 {label_a}</span>"
        verdict_sub = f"Leads by <strong>{margin:.0f}</strong> net score points · {cmp_days}d window"
    else:
        winner_html = f"<span style='color:#ffd54f;'>🏆 {label_b}</span>"
        verdict_sub = f"Leads by <strong>{margin:.0f}</strong> net score points · {cmp_days}d window"

    st.markdown(f"""
    <div class="verdict-box">
        <div class="verdict-eyebrow">Overall Technical Verdict</div>
        <div class="verdict-winner">{winner_html}</div>
        <div class="verdict-sub">{verdict_sub}</div>
        <div style="margin-top:1rem;display:flex;justify-content:center;gap:2rem;font-size:0.9rem;">
            <div><span class="cmp-badge-a">{sym_a}</span> &nbsp;<strong style="color:#40c4ff;">{score_a:+d}</strong></div>
            <div><span class="cmp-badge-b">{sym_b}</span> &nbsp;<strong style="color:#ffd54f;">{score_b:+d}</strong></div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Disclaimer:</strong> This comparison is for informational purposes only and does not constitute financial advice.
        Always do your own research before making investment decisions.
    </div>""", unsafe_allow_html=True)



# ============================
# DCA Simulator Tab
# ============================
def render_dca_tab():
    st.markdown("### 💰 DCA Simulator")
    st.markdown('<p class="small-note">Simulate investing a fixed amount at regular intervals over historical price data. See exactly what your strategy would have returned.</p>', unsafe_allow_html=True)

    # ── Controls ──────────────────────────────────────────────────
    d1, d2, d3 = st.columns([3, 2, 2])
    with d1:
        dca_coin_key = st.selectbox("Coin", list(DEFAULT_COINS.keys()), key="dca_coin")
    with d2:
        dca_amount = st.number_input("Amount per buy (USD)", min_value=1.0, value=100.0, step=10.0, key="dca_amt")
    with d3:
        dca_freq = st.selectbox("Buy frequency", ["Daily", "Weekly", "Bi-weekly", "Monthly"], index=2, key="dca_freq")

    # Period row — number input + radio shortcuts (single native widget, no state conflicts)
    st.markdown('<div style="margin-top:0.2rem;"></div>', unsafe_allow_html=True)
    p_col, r_col = st.columns([2, 5])
    with r_col:
        preset_label = st.radio(
            "Quick select",
            options=["1 week", "1 month", "3 months", "6 months", "9 months", "1 year", "Custom"],
            index=3,
            horizontal=True,
            key="dca_preset_radio",
        )
    preset_map = {
        "1 week": 7, "1 month": 30, "3 months": 90,
        "6 months": 180, "9 months": 270, "1 year": 365,
    }
    with p_col:
        default_val = preset_map.get(preset_label, 180)
        dca_period = st.number_input(
            "Period (days)",
            min_value=7, max_value=730,
            value=default_val,
            step=1,
            key="dca_period_input",
            disabled=(preset_label != "Custom"),
            help="Select 'Custom' in the radio to type any number of days",
        )
    # If a preset is selected use its value; only use the input when Custom is chosen
    if preset_label != "Custom":
        dca_period = preset_map[preset_label]

    dca_info   = DEFAULT_COINS[dca_coin_key]
    dca_sym    = dca_coin_key.split("—")[0].strip().split()[0]
    dca_name   = dca_info["name"]

    try:
        with st.spinner(f"Loading {dca_sym} history..."):
            raw_daily = get_daily_data(dca_info["id"])
            hist      = slice_last_days(raw_daily, dca_period).copy()

        if len(hist) < 5:
            st.warning("Not enough historical data for this period.")
            return

        # ── Build DCA schedule ────────────────────────────────────
        freq_map = {"Daily": 1, "Weekly": 7, "Bi-weekly": 14, "Monthly": 30}
        interval = freq_map[dca_freq]

        # Select buy dates at the chosen interval
        buy_dates = hist.iloc[::interval].copy()

        # Simulation state
        total_invested = 0.0
        total_coins    = 0.0
        purchases      = []

        for _, row in buy_dates.iterrows():
            price_at_buy  = row["price"]
            coins_bought  = dca_amount / price_at_buy
            total_invested += dca_amount
            total_coins    += coins_bought
            purchases.append({
                "date":         row["timestamp"],
                "price":        price_at_buy,
                "coins_bought": coins_bought,
                "usd_spent":    dca_amount,
                "total_coins":  total_coins,
                "total_invested": total_invested,
                "portfolio_value": total_coins * price_at_buy,
            })

        df_purchases = pd.DataFrame(purchases)

        # Current value uses last available price
        current_price   = hist["price"].iloc[-1]
        current_value   = total_coins * current_price
        total_profit    = current_value - total_invested
        roi_pct         = (total_profit / total_invested * 100) if total_invested > 0 else 0
        avg_buy_price   = total_invested / total_coins if total_coins > 0 else 0
        num_buys        = len(df_purchases)
        price_vs_avg    = ((current_price - avg_buy_price) / avg_buy_price * 100) if avg_buy_price > 0 else 0

        # Build portfolio value over time (mark-to-market each day)
        hist = hist.copy()
        hist["portfolio_value"] = np.nan
        hist["total_invested"]  = np.nan
        running_coins    = 0.0
        running_invested = 0.0
        buy_idx = 0
        buy_rows = df_purchases.to_dict("records")

        for i, row in hist.iterrows():
            # Process any buys on or before this date
            while buy_idx < len(buy_rows) and buy_rows[buy_idx]["date"] <= row["timestamp"]:
                running_coins    += buy_rows[buy_idx]["coins_bought"]
                running_invested += buy_rows[buy_idx]["usd_spent"]
                buy_idx += 1
            hist.at[i, "portfolio_value"] = running_coins * row["price"]
            hist.at[i, "total_invested"]  = running_invested

        # ── Stat cards ────────────────────────────────────────────
        profit_color    = "green" if total_profit >= 0 else "red"
        roi_color       = "green" if roi_pct >= 0 else "red"
        avg_market_price = hist["price"].mean()          # simple mean of all daily prices in period
        dca_vs_market   = ((avg_buy_price - avg_market_price) / avg_market_price * 100) if avg_market_price > 0 else 0

        s1, s2, s3, s4 = st.columns(4)
        s5, s6, s7, s8 = st.columns(4)
        cards = [
            (s1, "Total Invested",    f"${total_invested:,.2f}",    f"{num_buys} purchases",           "blue"),
            (s2, "Current Value",     f"${current_value:,.2f}",     f"{total_coins:.6g} {dca_sym}",    "purple"),
            (s3, "Total P&L",         f"${total_profit:+,.2f}",     f"{roi_pct:+.1f}% ROI",            profit_color),
            (s4, "ROI",               f"{roi_pct:+.1f}%",           f"over {dca_period} days",         roi_color),
            (s5, "Your Avg Buy Price",format_price(avg_buy_price),  f"cost basis per {dca_sym}",       "gold"),
            (s6, "Market Avg Price",  format_price(avg_market_price),f"period TWAP",                   "blue"),
            (s7, "DCA vs Market Avg", f"{dca_vs_market:+.1f}%",     "your avg vs period avg price",    "green" if dca_vs_market <= 0 else "red"),
            (s8, "Price vs Your Avg", f"{price_vs_avg:+.1f}%",      "current price vs your cost",      "green" if price_vs_avg >= 0 else "red"),
        ]
        for col, label, value, sub, color in cards:
            with col:
                st.markdown(f"""
                <div class="dca-stat-card {color}">
                    <div class="dca-stat-label">{label}</div>
                    <div class="dca-stat-value">{value}</div>
                    <div class="dca-stat-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Main chart: portfolio value vs invested ────────────────
        fig_dca = go.Figure()

        fig_dca.add_trace(go.Scatter(
            x=hist["timestamp"], y=hist["total_invested"],
            name="Total Invested", fill="tozeroy",
            fillcolor="rgba(26,107,255,0.08)",
            line=dict(color="#1a6bff", width=1.5, dash="dash"),
            hovertemplate="Invested: <b>$%{y:,.2f}</b><extra></extra>",
        ))
        fig_dca.add_trace(go.Scatter(
            x=hist["timestamp"], y=hist["portfolio_value"],
            name="Portfolio Value", fill="tonexty",
            fillcolor="rgba(0,230,118,0.10)" if total_profit >= 0 else "rgba(255,82,82,0.10)",
            line=dict(color="#00e676" if total_profit >= 0 else "#ff5252", width=2.5),
            hovertemplate="Value: <b>$%{y:,.2f}</b><extra></extra>",
        ))

        # Mark each buy as a dot on the portfolio value line
        fig_dca.add_trace(go.Scatter(
            x=df_purchases["date"],
            y=df_purchases["portfolio_value"],
            mode="markers",
            name="Buy event",
            marker=dict(color="#ffd54f", size=7, symbol="circle",
                        line=dict(color="#080c14", width=1.5)),
            hovertemplate=(
                "<b>Buy #%{pointNumber}</b><br>"
                "Date: %{x|%Y-%m-%d}<br>"
                "Price: <b>$%{customdata[0]:.6g}</b><br>"
                "Bought: <b>%{customdata[1]:.6g} " + dca_sym + "</b><br>"
                "Total invested: <b>$%{customdata[2]:,.2f}</b><extra></extra>"
            ),
            customdata=df_purchases[["price","coins_bought","total_invested"]].values,
        ))

        # Average buy price horizontal line
        fig_dca.add_hline(
            y=avg_buy_price * (total_coins),
            line=dict(color="#ffb74d", width=1, dash="dot"),
            annotation_text=f"Avg cost basis",
            annotation_font_color="#ffb74d",
        )

        BG = "#080c14"; PANEL = "#0d1117"; GRID = "rgba(255,255,255,0.06)"
        fig_dca.update_layout(
            height=420,
            paper_bgcolor=BG, plot_bgcolor=PANEL,
            font=dict(family="Inter, sans-serif", color="#c0cfe8"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#0d1117", bordercolor="#2a4080",
                            font=dict(color="#e8ecf0", size=12)),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                        bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                       tickfont=dict(color="#6b7a99"), linecolor="#1a2540"),
            yaxis=dict(title="USD", showgrid=True, gridcolor=GRID, zeroline=False,
                       tickprefix="$", tickfont=dict(color="#6b7a99"), linecolor="#1a2540"),
            margin=dict(l=60, r=40, t=40, b=40),
            title=dict(text=f"{dca_name} ({dca_sym}) — {dca_freq} DCA · {dca_period} Days",
                       font=dict(color="#6b7a99", size=12)),
        )
        st.plotly_chart(fig_dca, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})

        # ── Price chart with avg buy line ─────────────────────────
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=hist["timestamp"], y=hist["price"],
            name="Price", line=dict(color="#40c4ff", width=2),
            hovertemplate="Price: <b>$%{y:.6g}</b><extra></extra>",
        ))
        fig_price.add_hline(
            y=avg_buy_price,
            line=dict(color="#ffd54f", width=1.5, dash="dash"),
            annotation_text=f"Your avg buy {format_price(avg_buy_price)}",
            annotation_font_color="#ffd54f",
            annotation_position="right",
        )
        fig_price.add_hline(
            y=avg_market_price,
            line=dict(color="#40c4ff", width=1.2, dash="dot"),
            annotation_text=f"Period market avg {format_price(avg_market_price)}",
            annotation_font_color="#40c4ff",
            annotation_position="left",
        )
        fig_price.add_trace(go.Scatter(
            x=df_purchases["date"], y=df_purchases["price"],
            mode="markers", name="Buy at price",
            marker=dict(color="#ffd54f", size=8, symbol="triangle-up",
                        line=dict(color="#080c14", width=1.5)),
            hovertemplate="Buy price: <b>$%{y:.6g}</b><extra></extra>",
        ))
        fig_price.update_layout(
            height=300,
            paper_bgcolor=BG, plot_bgcolor=PANEL,
            font=dict(family="Inter, sans-serif", color="#c0cfe8"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#0d1117", bordercolor="#2a4080",
                            font=dict(color="#e8ecf0", size=12)),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                        bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                       tickfont=dict(color="#6b7a99"), linecolor="#1a2540"),
            yaxis=dict(title="Price (USD)", showgrid=True, gridcolor=GRID, zeroline=False,
                       tickfont=dict(color="#6b7a99"), linecolor="#1a2540"),
            margin=dict(l=60, r=40, t=30, b=40),
            title=dict(text="Price History with Buy Points",
                       font=dict(color="#6b7a99", size=12)),
        )
        st.plotly_chart(fig_price, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})

        # ── Insights ──────────────────────────────────────────────
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Strategy Insights</div>', unsafe_allow_html=True)

        insights = []

        if roi_pct > 0:
            insights.append(("green", f"✅ Your {dca_freq.lower()} DCA strategy returned <strong>{roi_pct:+.1f}%</strong> over {dca_period} days, turning ${total_invested:,.0f} into ${current_value:,.0f}."))
        else:
            insights.append(("red", f"📉 Your {dca_freq.lower()} DCA strategy is down <strong>{roi_pct:.1f}%</strong> over {dca_period} days. You invested ${total_invested:,.0f}, currently worth ${current_value:,.0f}."))

        if price_vs_avg > 0:
            insights.append(("green", f"📈 Current price ({format_price(current_price)}) is <strong>{price_vs_avg:+.1f}%</strong> above your average buy price of {format_price(avg_buy_price)} — you are in profit on your cost basis."))
        else:
            insights.append(("red", f"📉 Current price ({format_price(current_price)}) is <strong>{price_vs_avg:.1f}%</strong> below your average buy price of {format_price(avg_buy_price)} — you are below your cost basis."))

        if dca_vs_market <= 0:
            insights.append(("green", f"📊 Your average buy price ({format_price(avg_buy_price)}) is <strong>{abs(dca_vs_market):.1f}% below</strong> the period's market average price ({format_price(avg_market_price)}) — your DCA timing was better than average."))
        else:
            insights.append(("red", f"📊 Your average buy price ({format_price(avg_buy_price)}) is <strong>{dca_vs_market:.1f}% above</strong> the period's market average price ({format_price(avg_market_price)}) — you paid slightly above the average price."))

        # Best and worst buys
        best_buy = df_purchases.loc[df_purchases["price"].idxmin()]
        worst_buy = df_purchases.loc[df_purchases["price"].idxmax()]
        best_gain = (current_price - best_buy["price"]) / best_buy["price"] * 100
        worst_gain = (current_price - worst_buy["price"]) / worst_buy["price"] * 100
        insights.append(("gold", f"🏆 Best buy: {best_buy['date'].strftime('%b %d, %Y')} at {format_price(best_buy['price'])} — now <strong>{best_gain:+.1f}%</strong> from that entry."))
        insights.append(("gold" if worst_gain > 0 else "red", f"⚠️ Highest buy: {worst_buy['date'].strftime('%b %d, %Y')} at {format_price(worst_buy['price'])} — now <strong>{worst_gain:+.1f}%</strong> from that entry."))

        # Lump sum comparison
        first_price = hist["price"].iloc[0]
        lump_coins  = total_invested / first_price
        lump_value  = lump_coins * current_price
        lump_roi    = (lump_value - total_invested) / total_invested * 100
        if lump_roi > roi_pct:
            insights.append(("red", f"💡 A lump-sum investment of ${total_invested:,.0f} on day 1 at {format_price(first_price)} would be worth ${lump_value:,.2f} today (<strong>{lump_roi:+.1f}%</strong>) — outperforming DCA by <strong>{lump_roi - roi_pct:.1f}%</strong>."))
        else:
            insights.append(("green", f"💡 DCA <strong>outperformed</strong> a lump-sum investment by <strong>{roi_pct - lump_roi:.1f}%</strong>. Lump sum at {format_price(first_price)} would be worth ${lump_value:,.2f} ({lump_roi:+.1f}%)."))

        for color, text in insights:
            st.markdown(f'<div class="dca-insight {color}">{text}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Buy-by-buy table ──────────────────────────────────────
        with st.expander("📋 Full purchase history"):
            display_df = df_purchases[["date", "price", "coins_bought", "usd_spent",
                                        "total_coins", "total_invested", "portfolio_value"]].copy()
            display_df["date"]           = display_df["date"].dt.strftime("%Y-%m-%d")
            display_df["price"]          = display_df["price"].apply(format_price)
            display_df["coins_bought"]   = display_df["coins_bought"].apply(lambda v: f"{v:.6g}")
            display_df["usd_spent"]      = display_df["usd_spent"].apply(lambda v: f"${v:,.2f}")
            display_df["total_coins"]    = display_df["total_coins"].apply(lambda v: f"{v:.6g}")
            display_df["total_invested"] = display_df["total_invested"].apply(lambda v: f"${v:,.2f}")
            display_df["portfolio_value"]= display_df["portfolio_value"].apply(lambda v: f"${v:,.2f}")
            display_df.columns = ["Date", "Price Paid", f"{dca_sym} Bought",
                                   "USD Spent", f"Total {dca_sym}", "Total Invested", "Portfolio Value"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="disclaimer-box">
            ⚠️ <strong>Disclaimer:</strong> DCA simulation uses historical price data only. Past performance does not
            guarantee future results. This is not financial advice.
        </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error running DCA simulation: {e}")


def render_top_performers(coins):
    """Render the top 5 performers for the past 24 hours."""
    key   = "price_change_percentage_24h_in_currency"
    valid = [c for c in coins if c.get(key) is not None]
    top5  = sorted(valid, key=lambda c: c[key], reverse=True)[:5]

    if not top5:
        st.markdown('<div class="small-note">No data available.</div>', unsafe_allow_html=True)
        return

    max_abs    = max(abs(c[key]) for c in top5) or 1
    cards_html = ""
    for i, coin in enumerate(top5):
        pct       = coin[key]
        sym       = coin["symbol"].upper()
        name      = coin["name"]
        price_str = format_price(coin["current_price"])
        sign      = "pos" if pct >= 0 else "neg"
        arrow     = "▲" if pct >= 0 else "▼"
        bar_w     = min(int(abs(pct) / max_abs * 100), 100)
        cards_html += (
            f'<div class="perf-card">'
            f'<div class="perf-card-rank">#{i+1}</div>'
            f'<div class="perf-card-sym">{sym}</div>'
            f'<div class="perf-card-name">{name}</div>'
            f'<div class="perf-card-price">{price_str}</div>'
            f'<div class="perf-card-pct {sign}">{arrow} {abs(pct):.2f}%</div>'
            f'<div class="perf-card-bar {sign}" style="width:{bar_w}%;"></div>'
            f'</div>'
        )
    st.markdown(f'<div class="perf-grid">{cards_html}</div>', unsafe_allow_html=True)



# ============================
# APP ENTRY POINT
# ============================
st.markdown("""
<div class="page-hero">
    <h1>Crypto Market Dashboard</h1>
    <div class="sub">
        Multi-timeframe analysis <span>1d → 180d</span> &nbsp;·&nbsp;
        ATR price targets &nbsp;·&nbsp; Pattern detection &nbsp;·&nbsp;
        OBV &nbsp;·&nbsp; Stochastic RSI
    </div>
</div>
""", unsafe_allow_html=True)

tab_dashboard, tab_compare, tab_dca = st.tabs(["📊  Dashboard", "⚖️  Compare", "💰  DCA Simulator"])

# ── DASHBOARD TAB ──────────────────────────────────────────────────────────
with tab_dashboard:

    # ── Top Performers ────────────────────────────────────────────────────
    top_coins = get_top_performers()
    # Pre-warm BTC daily data — most common coin, reuses 6h cache on all subsequent tab visits
    try:
        get_daily_data("bitcoin")
    except Exception:
        pass
    if top_coins:
        st.markdown('<div class="top-perf-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="top-perf-title">🏆 Top Performers &nbsp;·&nbsp; 24h</div>', unsafe_allow_html=True)
        render_top_performers(top_coins)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Top Gainers (24h) ─────────────────────────────────────────────────
    if top_coins:
        tf_key_24h = "price_change_percentage_24h_in_currency"
        valid_24h  = [c for c in top_coins if c.get(tf_key_24h) is not None]
        top3       = sorted(valid_24h, key=lambda c: c[tf_key_24h], reverse=True)[:3]
        if top3:
            st.markdown('<div class="gainers-label">\U0001f680 Top Gainers \u00b7 24h</div>', unsafe_allow_html=True)
            g1, g2, g3 = st.columns(3)
            medals = [("r1","\U0001f947"), ("r2","\U0001f948"), ("r3","\U0001f949")]
            for col, coin, (rk, medal) in zip([g1, g2, g3], top3, medals):
                pct   = coin[tf_key_24h]
                sym   = coin["symbol"].upper()
                name  = coin["name"]
                price = format_price(coin["current_price"])
                card  = (
                    '<div class="gainer-card">'
                    f'<div class="gainer-rank {rk}">{medal}</div>'
                    '<div class="gainer-body">'
                    f'<div class="gainer-sym">{sym}</div>'
                    f'<div class="gainer-name">{name}</div>'
                    '</div>'
                    '<div class="gainer-right">'
                    f'<div class="gainer-pct">\u25b2 {pct:.2f}%</div>'
                    f'<div class="gainer-price">{price}</div>'
                    '</div>'
                    '</div>'
                )
                with col:
                    st.markdown(card, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        chosen_label = st.selectbox("Choose a coin", list(DEFAULT_COINS.keys()))
    with c2:
        days = st.selectbox("Chart period (days)", [1, 7, 14, 30, 90, 180, 365], index=4)
    with c3:
        st.write(""); st.write("")
        if st.button("↺  Refresh", use_container_width=True):
            get_daily_data.clear()
            get_hourly_data.clear()
            get_top_performers.clear()
            st.rerun()

    coin_info       = DEFAULT_COINS[chosen_label]
    coin_name       = coin_info["name"]
    coin_id         = coin_info["id"]
    selected_symbol = chosen_label.split("—")[0].strip().split()[0]
    coin_label      = f"{coin_name} ({selected_symbol})"

    try:
        daily_data  = get_daily_data(coin_id)
        hourly_data = get_hourly_data(coin_id)

        chart_raw  = slice_last_days(hourly_data if days <= 14 else daily_data, days)
        chart_data = add_indicators(chart_raw)
        analysis   = analyze_prices(chart_data)

        mtf = {}
        for tf in ALL_TIMEFRAMES:
            tf_src   = hourly_data if tf <= 14 else daily_data
            tf_slice = slice_last_days(tf_src, tf)
            tf_slice = add_indicators(tf_slice)
            mtf[tf]  = analyze_prices(tf_slice)

        # ── Metric strip ──────────────────────────────────────────────────
        pct      = analysis['pct_change']
        pct_col  = "#00e676" if pct >= 0 else "#ff5252"
        pct_icon = "▲" if pct >= 0 else "▼"
        rsi_d    = f"{analysis['rsi']:.1f}"    if pd.notna(analysis['rsi'])     else "N/A"
        sk_d     = f"{analysis['stoch_k']:.0f}" if pd.notna(analysis['stoch_k']) else "N/A"
        rc       = recommendation_class(analysis['recommendation'])

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">Current Price</div>
                <div class="metric-value">{format_price(analysis['price'])}</div>
            </div>''', unsafe_allow_html=True)
        with m2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">Period Return</div>
                <div class="metric-value-small" style="color:{pct_col};">{pct_icon} {abs(pct):.2f}%</div>
            </div>''', unsafe_allow_html=True)
        with m3:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">RSI 14</div>
                <div class="metric-value-small">{rsi_d}</div>
            </div>''', unsafe_allow_html=True)
        with m4:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">Stoch RSI</div>
                <div class="metric-value-small">{sk_d}</div>
            </div>''', unsafe_allow_html=True)
        with m5:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">Bull / Bear</div>
                <div class="metric-value-small">
                    <span class="signal-bull">{analysis['bull_score']}</span>
                    <span style="color:#1a2540;"> / </span>
                    <span class="signal-bear">{analysis['bear_score']}</span>
                </div>
            </div>''', unsafe_allow_html=True)
        with m6:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-title">Signal</div>
                <div style="margin-top:0.4rem;"><span class="rec-badge {rc}">{analysis['recommendation']}</span></div>
            </div>''', unsafe_allow_html=True)

        # ── Chart ─────────────────────────────────────────────────────────
        fig = build_figure(chart_data, coin_label, days,
                           analysis["recommendation"], analysis["support"], analysis["resistance"])
        st.plotly_chart(fig, use_container_width=True, config={
            "scrollZoom": True,
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
            "toImageButtonOptions": {"format": "png", "filename": coin_id, "scale": 2},
        })

        # ── Bottom panels ─────────────────────────────────────────────────
        left, right = st.columns([1.35, 1])

        with left:
            support_str    = format_price(analysis['support'])    if pd.notna(analysis['support'])    else "—"
            resistance_str = format_price(analysis['resistance']) if pd.notna(analysis['resistance']) else "—"
            vol_lbl        = analysis['volatility_label']
            ts_str         = analysis['latest_time'].strftime('%Y-%m-%d %H:%M UTC')

            st.markdown(f"""
            <div class="section-box">
                <div class="section-title">Market Summary</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem 1.5rem;font-size:0.9rem;line-height:1.8;">
                    <div><span class="small-note">Coin</span><br><strong>{coin_label}</strong></div>
                    <div><span class="small-note">Last update</span><br><strong>{ts_str}</strong></div>
                    <div><span class="small-note">Period change</span><br><strong style="color:{pct_col};">{pct:+.2f}%</strong></div>
                    <div><span class="small-note">Volatility</span><br><strong>{vol_lbl}</strong></div>
                    <div><span class="small-note">Support</span><br><strong>{support_str}</strong></div>
                    <div><span class="small-note">Resistance</span><br><strong>{resistance_str}</strong></div>
                    <div><span class="small-note">Trend</span><br><span class="{sentiment_class(analysis['trend_text'])}">{analysis['trend_text']}</span></div>
                    <div><span class="small-note">EMA structure</span><br><span class="{sentiment_class(analysis['ema_text'])}">{analysis['ema_text']}</span></div>
                    <div><span class="small-note">RSI state</span><br><span class="{sentiment_class(analysis['rsi_text'])}">{analysis['rsi_text']}</span></div>
                    <div><span class="small-note">MACD</span><br><span class="{sentiment_class(analysis['macd_text'])}">{analysis['macd_text']}</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Detected Patterns & Signals</div>', unsafe_allow_html=True)
            render_patterns(analysis["patterns"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Price Target Outlooks</div>', unsafe_allow_html=True)
            st.markdown('<div class="small-note" style="margin-bottom:0.6rem;">Signal breakdown</div>', unsafe_allow_html=True)
            for line in analysis["interpretation"]:
                st.markdown(f'<div class="small-note" style="padding:0.15rem 0;">• {line}</div>', unsafe_allow_html=True)
            render_outlook("Short-term (next few periods)", analysis["short_term_outlook"])
            render_outlook("Medium-term (1–2 weeks)",       analysis["medium_term_outlook"])
            render_outlook("Long-term (1–3 months)",        analysis["long_term_outlook"])
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Multi-Timeframe View</div>', unsafe_allow_html=True)
            st.markdown('<div class="small-note" style="margin-bottom:0.4rem;">Short-term · hourly data</div>', unsafe_allow_html=True)
            for tf in SHORT_TIMEFRAMES:
                render_tf_row(tf, mtf[tf])
            st.markdown('<div class="small-note" style="margin:0.9rem 0 0.4rem;">Medium / long-term · daily data</div>', unsafe_allow_html=True)
            for tf in MEDIUM_TIMEFRAMES:
                render_tf_row(tf, mtf[tf])

            all_diffs = [mtf[tf]["score_diff"] for tf in ALL_TIMEFRAMES]
            n_bull    = sum(1 for d in all_diffs if d > 10)
            n_bear    = sum(1 for d in all_diffs if d < -10)
            total     = len(ALL_TIMEFRAMES)
            if n_bull >= 5:
                agree_html = f"<span class='signal-bull'>Strong bullish consensus · {n_bull}/{total} TFs</span>"
            elif n_bear >= 5:
                agree_html = f"<span class='signal-bear'>Strong bearish consensus · {n_bear}/{total} TFs</span>"
            elif n_bull > n_bear:
                agree_html = f"<span class='signal-bull'>Mild bullish lean · {n_bull}B vs {n_bear}S</span>"
            elif n_bear > n_bull:
                agree_html = f"<span class='signal-bear'>Mild bearish lean · {n_bear}S vs {n_bull}B</span>"
            else:
                agree_html = "<span class='signal-neutral'>Timeframes split — no consensus</span>"
            st.markdown(f'<div style="margin-top:1rem;font-size:0.88rem;">Consensus: {agree_html}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            p      = analysis["price"]
            atr    = analysis["atr"]
            bull_t = format_price(p + atr * 3)
            bear_t = format_price(clamp_price(p - atr * 3))
            sup_s  = format_price(analysis['support']) if pd.notna(analysis['support']) else None

            st.markdown(f"""
            <div class="section-box">
                <div class="section-title">Market Scenario</div>
                <div style="font-size:0.9rem;line-height:1.7;color:#c0cfe8;">{analysis['scenario']}</div>
                <div style="margin-top:1rem;display:flex;flex-direction:column;gap:0.5rem;">
                    <div style="background:#001a0d;border:1px solid #004d20;border-radius:10px;padding:0.7rem 1rem;font-size:0.88rem;">
                        🟢 <strong>Bull case:</strong> {"Hold above " + sup_s + " → target " if sup_s else "Buying pressure → "}{bull_t}
                    </div>
                    <div style="background:#1a0000;border:1px solid #4d0000;border-radius:10px;padding:0.7rem 1rem;font-size:0.88rem;">
                        🔴 <strong>Bear case:</strong> {"Break of " + sup_s + " → risk " if sup_s else "Selling pressure → "}{bear_t}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
            csv = chart_data.to_csv(index=False).encode("utf-8")
            st.download_button("⬇  Download CSV", data=csv,
                               file_name=f"{coin_id}_analysis.csv", mime="text/csv",
                               use_container_width=True)
            png_bytes = figure_to_png_bytes(fig)
            st.download_button("⬇  Download Chart PNG", data=png_bytes,
                               file_name=f"{coin_id}_chart.png", mime="image/png",
                               use_container_width=True,
                               disabled=len(png_bytes.read()) == 0,
                               help="Requires the 'kaleido' package for PNG export")
            st.markdown('<div class="small-note" style="margin-top:0.6rem;">🟢 Bullish &nbsp;·&nbsp; 🔴 Bearish &nbsp;·&nbsp; 🟡 Neutral</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer-box">
            ⚠️ <strong>Disclaimer:</strong> This dashboard is for informational and educational purposes only.
            Nothing here constitutes financial or investment advice. Crypto markets are highly volatile.
            Past signals do not guarantee future results. Always do your own research.
        </div>""", unsafe_allow_html=True)

    except Exception as e:
        err = str(e)
        if "rate limit" in err.lower() or "429" in err:
            st.warning(
                "⏳ **CoinGecko rate limit hit.** "
                "The free API allows ~30 calls/minute. "
                "Cached data expires automatically — wait ~60 seconds and click **↺ Refresh**."
            )
        else:
            st.error(f"Error loading data: {e}")

# ── COMPARE TAB ────────────────────────────────────────────────────────────
with tab_compare:
    render_compare_tab()

# ── DCA TAB ────────────────────────────────────────────────────────────────
with tab_dca:
    render_dca_tab()
