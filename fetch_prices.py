"""
fetch_prices.py
---------------
Pre-fetches all price data for Maven Securities follow-on deal analysis.
Run this script ONCE locally to build the returns cache.
Output: returns_cache.parquet, data_quality_log.txt
"""

import pandas as pd
import numpy as np
import yfinance as yf
import time
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data_quality_log.txt", mode="w"),
    ],
)
log = logging.getLogger(__name__)

DATA_PATH = "data/CMG Data - Last 4Y and YTD FOs in North Asia v2.xlsx"
CACHE_OUT  = "returns_cache.parquet"

# Trading-day horizons and labels
HORIZONS = {
    "D1_open":  ("open",  1),
    "D1_close": ("close", 1),
    "D1_vwap":  ("vwap",  1),
    "D2_close": ("close", 2),
    "D5_close": ("close", 5),
    "D7_close": ("close", 7),
    "D14_close":("close", 14),
    "D30_close":("close", 30),
    "D63_close":("close", 63),
    "D126_close":("close",126),
}

HORIZON_LABELS = {
    "D1_open":   "D1 Open",
    "D1_close":  "D1 Close",
    "D1_vwap":   "D1 VWAP",
    "D2_close":  "D2",
    "D5_close":  "D5",
    "D7_close":  "D7",
    "D14_close": "D14",
    "D30_close": "D30",
    "D63_close": "D63",
    "D126_close":"D126",
}

EXCHANGE_SUFFIX = {
    "XHKG": ".HK",
    "XTKS": ".T",
    "XKRX": ".KS",
    "XSHG": ".SS",
}


def load_and_clean():
    df = pd.read_excel(DATA_PATH, sheet_name="Market Pulse")

    # Filter to North Asia
    df = df[df["Exchange Country"].isin(["HK", "CN", "JP", "KR"])].copy()
    log.info(f"North Asia deals: {len(df)}")

    # Pricing Date — already datetime from pandas
    df["Pricing Date"] = pd.to_datetime(df["Pricing Date"])
    df["Year"] = df["Pricing Date"].dt.year

    # Region mapping
    region_map = {"HK": "HK/China", "CN": "HK/China", "JP": "Japan", "KR": "Korea"}
    df["Region"] = df["Exchange Country"].map(region_map)

    # Sector regrouping
    # Basic Materials is sparse in North Asia; keep as-is since it's distinct.
    # Communication Services → keep (telcos, media, internet)
    # Consumer Cyclical → keep
    # Consumer Defensive → keep
    # Energy → keep (oil & gas, utilities)
    # Financial Services → keep (banks, insurance, asset mgmt)
    # Healthcare → keep
    # Industrials → keep (manufacturing, logistics)
    # Real Estate → keep (REITs, developers — large in HK/China)
    # Technology → keep
    # Utilities → merge into Energy (both are capital-intensive infrastructure)
    # NaN → "Other"
    sector_remap = {
        "Utilities": "Energy & Utilities",
        "Energy": "Energy & Utilities",
        "Basic Materials": "Basic Materials",
    }
    df["Sector"] = df["Sector"].fillna("Other")
    df["Sector"] = df["Sector"].replace(sector_remap)

    # Deal size buckets (USD)
    def size_bucket(x):
        if pd.isna(x): return np.nan
        if x < 100e6:  return "Small (<$100M)"
        if x < 500e6:  return "Mid ($100-500M)"
        return "Large (>$500M)"

    # Market cap buckets (USD)
    def mcap_bucket(x):
        if pd.isna(x): return np.nan
        if x < 1e9:    return "Small Cap (<$1B)"
        if x < 10e9:   return "Mid Cap ($1-10B)"
        return "Large Cap (>$10B)"

    df["Deal Size Bucket"] = df["Gross Proceeds Total $"].apply(size_bucket)
    df["MktCap Bucket"]    = df["Post-Offering Mkt. Cap $"].apply(mcap_bucket)

    # Build yfinance ticker
    def make_yf_ticker(row):
        exch   = row["Exchange"]
        ticker = str(row["Ticker"]).strip()
        suffix = EXCHANGE_SUFFIX.get(exch)
        if suffix is None:
            return None
        if exch == "XHKG":
            # Zero-pad to 4 digits
            try:
                ticker = str(int(ticker)).zfill(4)
            except ValueError:
                pass
        return ticker + suffix

    df["yf_ticker"] = df.apply(make_yf_ticker, axis=1)
    df = df.reset_index(drop=True)
    return df


def fetch_ticker_data(yf_ticker, start_date, end_date):
    """
    Download OHLCV (raw, no auto-adjust) and split history for a single ticker.
    Returns (hist_df, splits_series) or (None, None) on failure.

    We intentionally use auto_adjust=False to get raw nominal prices.
    Split adjustments are then applied manually to the offer price so that
    returns are not distorted by future stock splits or dividend adjustments.
    """
    try:
        t = yf.Ticker(yf_ticker)
        hist = t.history(
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            auto_adjust=False,   # raw prices — no backward split/div adjustment
            actions=True,        # include splits column in the result
        )
        if hist.empty:
            return None, None
        hist.index = pd.to_datetime(hist.index).tz_localize(None).normalize()

        # Also fetch the full split history (used for post-deal split adjustment)
        splits = t.splits
        if splits is not None and not splits.empty:
            splits.index = pd.to_datetime(splits.index).tz_localize(None).normalize()
        else:
            splits = pd.Series(dtype=float)

        return hist, splits
    except Exception as e:
        log.warning(f"  yfinance error for {yf_ticker}: {e}")
        return None, None


def cumulative_split_factor(splits, after_date, up_to_date):
    """
    Product of all split factors in `splits` that occurred strictly after
    `after_date` and on or before `up_to_date`.

    A split factor of 3 means 3-for-1 split (price drops by 3×, shares triple).
    A reverse split of 0.1 means 1-for-10 (price rises 10×, shares decrease).

    We use this to adjust the offer price forward so it is comparable to the
    raw (unadjusted) horizon price:
        adjusted_offer = offer_price / cumulative_split_factor
    """
    if splits.empty:
        return 1.0
    mask = (splits.index > after_date) & (splits.index <= up_to_date)
    relevant = splits[mask]
    if relevant.empty:
        return 1.0
    factor = float(relevant.prod())
    return factor if factor > 0 else 1.0


def get_nth_trading_day_price(hist, pricing_date, n, price_type):
    """
    Return the price on the Nth trading day after pricing_date.
    price_type: 'open', 'close', 'vwap'
    Also returns the actual date of that trading day (for split adjustment).
    Returns (price, date) or (nan, None).
    """
    later = hist[hist.index > pricing_date]
    if len(later) < n:
        return np.nan, None
    row     = later.iloc[n - 1]
    horizon_date = later.index[n - 1]
    if price_type == "open":
        px = float(row["Open"])
    elif price_type == "close":
        px = float(row["Close"])
    elif price_type == "vwap":
        px = float((row["High"] + row["Low"] + row["Close"]) / 3)
    else:
        return np.nan, None
    return px, horizon_date


def compute_returns(df):
    """
    For each deal, fetch price data and compute returns at all horizons.
    Uses raw (unadjusted) prices from yfinance with manual split correction
    to avoid distortion from post-deal stock splits and dividend adjustments.
    """
    for h in HORIZONS:
        df[f"ret_{h}"] = np.nan

    ticker_groups = {}
    for idx, row in df.iterrows():
        if pd.isna(row["yf_ticker"]):
            continue
        t = row["yf_ticker"]
        if t not in ticker_groups:
            ticker_groups[t] = {"indices": [], "min_date": row["Pricing Date"]}
        ticker_groups[t]["indices"].append(idx)
        if row["Pricing Date"] < ticker_groups[t]["min_date"]:
            ticker_groups[t]["min_date"] = row["Pricing Date"]

    unique_tickers = list(ticker_groups.keys())
    log.info(f"Unique yfinance tickers to download: {len(unique_tickers)}")

    failed_tickers = []

    for i, (yf_ticker, info) in enumerate(ticker_groups.items()):
        indices    = info["indices"]
        start_date = info["min_date"]
        fetch_start = start_date - pd.Timedelta(days=5)
        fetch_end   = pd.Timestamp.today() + pd.Timedelta(days=5)

        log.info(f"[{i+1}/{len(ticker_groups)}] Fetching {yf_ticker} "
                 f"({start_date.date()} → {fetch_end.date()}) "
                 f"— {len(indices)} deal(s)")

        hist, splits = fetch_ticker_data(yf_ticker, fetch_start, fetch_end)

        if hist is None or hist.empty:
            log.warning(f"  NO DATA for {yf_ticker}")
            failed_tickers.append((yf_ticker, "No data returned by yfinance"))
            time.sleep(0.5)
            continue

        for idx in indices:
            row          = df.loc[idx]
            pricing_date = row["Pricing Date"]
            offer_price  = row["Offer Price"]

            if pd.isna(offer_price) or offer_price <= 0:
                log.warning(f"  idx={idx} {yf_ticker} offer_price invalid: {offer_price}")
                continue

            # Split factor: product of ALL splits that occurred after the
            # pricing date, regardless of which horizon we are measuring.
            # Rationale: yfinance auto_adjust=False divides every historical
            # price by ALL future splits from that date to TODAY.  So if a
            # stock splits 5:1 in 2024, the Jan-2022 D1 price already appears
            # as 1/5 of its actual value.  The same divisor (5) must be
            # applied to the offer price so the ratio is meaningful.
            sf_all = cumulative_split_factor(
                splits, pricing_date, pd.Timestamp("2099-12-31")
            )
            adjusted_offer = offer_price / sf_all
            if adjusted_offer <= 0:
                continue

            for h_name, (ptype, n_days) in HORIZONS.items():
                px, horizon_date = get_nth_trading_day_price(
                    hist, pricing_date, n_days, ptype
                )
                if np.isnan(px) or horizon_date is None:
                    continue
                ret = (px / adjusted_offer) - 1
                ret = np.clip(ret, -2.0, 2.0)
                df.at[idx, f"ret_{h_name}"] = ret

        time.sleep(0.3)

    log.info(f"\n--- SUMMARY ---")
    log.info(f"Total deals: {len(df)}")
    log.info(f"Failed tickers: {len(failed_tickers)}")
    for t, reason in failed_tickers:
        log.info(f"  FAILED: {t} — {reason}")

    ret_cols = [f"ret_{h}" for h in HORIZONS]
    valid_mask = df[ret_cols].notna().any(axis=1)
    log.info(f"Deals with ≥1 valid return: {valid_mask.sum()} / {len(df)}")
    return df


def main():
    log.info("=== Maven Securities: Follow-On Unwind Price Fetch ===")
    df = load_and_clean()
    df = compute_returns(df)

    # Save cache
    df.to_parquet(CACHE_OUT, index=True)
    log.info(f"Saved returns cache to {CACHE_OUT}")

    # Quick sanity check
    ret_cols = [f"ret_{h}" for h in HORIZONS]
    log.info("\n=== Mean returns by horizon (all deals) ===")
    means = df[ret_cols].mean()
    for col, val in means.items():
        label = HORIZON_LABELS.get(col.replace("ret_", ""), col)
        log.info(f"  {label:10s}: {val:+.2%}")


if __name__ == "__main__":
    main()
