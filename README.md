# Maven Securities — North Asia Follow-On Unwind Analysis

Interactive Streamlit app analysing optimal unwind timing for 607 North Asia
follow-on offerings (HK/China, Japan, Korea) from 2022 to mid-2026.

## Deployment (Streamlit Community Cloud)

1. Fork/push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → select this repo → set main file to `app.py`
4. Deploy

The app uses `returns_cache.parquet` (pre-computed price data). To refresh
price data with latest quotes, run `python3 fetch_prices.py` locally.

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `fetch_prices.py` | Price data fetcher (run once locally) |
| `returns_cache.parquet` | Pre-computed returns (99% deal coverage) |
| `data/CMG Data...xlsx` | Source deal data |
| `unwind_strategy_writeup.md` | Professional writeup |
| `data_quality_log.txt` | Data quality and methodology notes |
