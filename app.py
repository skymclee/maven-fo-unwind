"""
Maven Securities — North Asia Follow-On Unwind Analysis
app.py  |  Streamlit web application
"""

import warnings
warnings.filterwarnings("ignore")

import os
import base64
import logging
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Maven Securities | North Asia FO Unwind — Sky Lee",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HORIZON_COLS = [
    "ret_D1_open", "ret_D1_close", "ret_D1_vwap",
    "ret_D2_close", "ret_D5_close", "ret_D7_close",
    "ret_D14_close", "ret_D30_close", "ret_D63_close", "ret_D126_close",
]
HORIZON_LABELS = {
    "ret_D1_open":   "D1 Open",
    "ret_D1_close":  "D1 Close",
    "ret_D1_vwap":   "D1 VWAP",
    "ret_D2_close":  "D2",
    "ret_D5_close":  "D5",
    "ret_D7_close":  "D7",
    "ret_D14_close": "D14",
    "ret_D30_close": "D30",
    "ret_D63_close": "D63",
    "ret_D126_close":"D126",
}
HORIZON_ORDER = list(HORIZON_LABELS.keys())
LABEL_ORDER   = [HORIZON_LABELS[h] for h in HORIZON_ORDER]

DEAL_SIZE_ORDER = ["Small (<$100M)", "Mid ($100-500M)", "Large (>$500M)"]
MCAP_ORDER      = ["Small Cap (<$1B)", "Mid Cap ($1-10B)", "Large Cap (>$10B)"]

NAVY   = "#1a3a5c"
GREEN  = "#2e7d4f"
COLORS = {
    "HK/China": NAVY,
    "Japan":    GREEN,
    "Korea":    "#4caf80",   # lighter green for the third series
}

PLOTLY_TEMPLATE = "plotly_white"
MAVEN_COLORS    = [NAVY, GREEN, "#4caf80", "#a8d5b5", "#8dafc4", "#c0cfe0"]
PLOTLY_FONT     = dict(family="Times New Roman, Times, serif", size=12, color="#0d1f2d")


@st.cache_data(show_spinner=False)
def _logo_b64():
    """Return base64-encoded Maven logo for inline HTML embedding."""
    logo_path = os.path.join(os.path.dirname(__file__), "maven_logo.png")
    if not os.path.exists(logo_path):
        logo_path = "maven_logo.png"
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
CACHE_PATH = "returns_cache.parquet"
DATA_PATH  = "data/CMG Data - Last 4Y and YTD FOs in North Asia v2.xlsx"

EXCHANGE_SUFFIX = {
    "XHKG": ".HK",
    "XTKS": ".T",
    "XKRX": ".KS",
    "XSHG": ".SS",
}


def _sector_remap(s):
    if pd.isna(s):
        return "Other"
    m = {"Utilities": "Energy & Utilities", "Energy": "Energy & Utilities"}
    return m.get(s, s)


def _size_bucket(x):
    if pd.isna(x): return np.nan
    if x < 100e6:  return "Small (<$100M)"
    if x < 500e6:  return "Mid ($100-500M)"
    return "Large (>$500M)"


def _mcap_bucket(x):
    if pd.isna(x): return np.nan
    if x < 1e9:    return "Small Cap (<$1B)"
    if x < 10e9:   return "Mid Cap ($1-10B)"
    return "Large Cap (>$10B)"


def _make_yf_ticker(row):
    exch   = row["Exchange"]
    ticker = str(row["Ticker"]).strip()
    suffix = EXCHANGE_SUFFIX.get(exch)
    if suffix is None:
        return None
    if exch == "XHKG":
        try:
            ticker = str(int(ticker)).zfill(4)
        except ValueError:
            pass
    return ticker + suffix


@st.cache_data(show_spinner="Loading data…")
def load_master():
    """
    Load master DataFrame. Prefers the pre-computed parquet cache (which has
    return columns) and falls back to Excel-only (no returns) if cache absent.
    """
    def _enrich(df):
        df["Pricing Date"] = pd.to_datetime(df["Pricing Date"])
        df["Year"]         = df["Pricing Date"].dt.year.astype(str)
        region_map = {"HK": "HK/China", "CN": "HK/China", "JP": "Japan", "KR": "Korea"}
        df["Region"]          = df["Exchange Country"].map(region_map)
        df["Sector"]          = df["Sector"].apply(_sector_remap)
        df["Deal Size Bucket"] = df["Gross Proceeds Total $"].apply(_size_bucket)
        df["MktCap Bucket"]    = df["Post-Offering Mkt. Cap $"].apply(_mcap_bucket)
        df["yf_ticker"]        = df.apply(_make_yf_ticker, axis=1)
        df["Deal Size $M"]     = (df["Gross Proceeds Total $"] / 1e6).round(1)
        df["MktCap $B"]        = (df["Post-Offering Mkt. Cap $"] / 1e9).round(2)
        for h in HORIZON_COLS:
            if h not in df.columns:
                df[h] = np.nan
        return df.reset_index(drop=True)

    if os.path.exists(CACHE_PATH):
        df = pd.read_parquet(CACHE_PATH)
        # Parquet from fetch_prices has all columns; just add derived ones if missing
        if "Year" not in df.columns:
            df = _enrich(df)
        else:
            # Ensure derived display columns exist
            if "Deal Size $M" not in df.columns:
                df["Deal Size $M"] = (df["Gross Proceeds Total $"] / 1e6).round(1)
            if "MktCap $B" not in df.columns:
                df["MktCap $B"] = (df["Post-Offering Mkt. Cap $"] / 1e9).round(2)
            df["Pricing Date"] = pd.to_datetime(df["Pricing Date"])
            df["Year"] = df["Pricing Date"].dt.year.astype(str)
            for h in HORIZON_COLS:
                if h not in df.columns:
                    df[h] = np.nan
        return df, True  # (dataframe, has_price_data)

    # Fallback: load from Excel, no returns
    df = pd.read_excel(DATA_PATH, sheet_name="Market Pulse")
    df = df[df["Exchange Country"].isin(["HK", "CN", "JP", "KR"])].copy()
    return _enrich(df), False


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------
def compute_metrics(df, groupby=None):
    """
    Compute mean, median, pct_positive, std, sharpe, n for each horizon.
    If groupby is given, returns a dict of {group_val: metrics_df}.
    """
    def _metrics_for_slice(sdf):
        rows = []
        for h in HORIZON_COLS:
            vals = sdf[h].dropna()
            n    = len(vals)
            if n == 0:
                rows.append(dict(horizon=h, label=HORIZON_LABELS[h], mean=np.nan,
                                 median=np.nan, pct_pos=np.nan, std=np.nan,
                                 sharpe=np.nan, n=0))
                continue
            mu    = vals.mean()
            med   = vals.median()
            pp    = (vals > 0).mean()
            sigma = vals.std()
            sh    = mu / sigma if sigma > 0 else np.nan
            rows.append(dict(horizon=h, label=HORIZON_LABELS[h], mean=mu,
                             median=med, pct_pos=pp, std=sigma, sharpe=sh, n=n))
        return pd.DataFrame(rows)

    if groupby is None:
        return _metrics_for_slice(df)

    result = {}
    for gval in df[groupby].dropna().unique():
        result[gval] = _metrics_for_slice(df[df[groupby] == gval])
    return result


def metrics_dict_to_df(metrics_dict):
    """Convert {group: metrics_df} to a single long DataFrame with a 'group' column."""
    frames = []
    for g, mdf in metrics_dict.items():
        mdf = mdf.copy()
        mdf["group"] = str(g)
        frames.append(mdf)
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------
def mean_return_line(mdf, title="Mean Return by Horizon", color_col=None):
    if color_col and "group" in mdf.columns:
        fig = px.line(
            mdf.dropna(subset=["mean"]),
            x="label", y="mean",
            color="group",
            markers=True,
            category_orders={"label": LABEL_ORDER},
            template=PLOTLY_TEMPLATE,
            title=title,
            color_discrete_sequence=MAVEN_COLORS,
        )
    else:
        fig = px.line(
            mdf.dropna(subset=["mean"]),
            x="label", y="mean",
            markers=True,
            category_orders={"label": LABEL_ORDER},
            template=PLOTLY_TEMPLATE,
            title=title,
            color_discrete_sequence=[NAVY],
        )
    fig.update_layout(
        xaxis_title="Horizon (trading days post-pricing)",
        yaxis_title="Mean Return (%)",
        yaxis_tickformat=".1%",
        legend_title=color_col or "",
        hovermode="x unified",
        font=PLOTLY_FONT,
    )
    fig.update_traces(hovertemplate="%{y:.2%}")
    return fig


def pct_positive_bar(mdf, title="% Deals with Positive Return"):
    fig = px.bar(
        mdf.dropna(subset=["pct_pos"]),
        x="label", y="pct_pos",
        text_auto=".0%",
        category_orders={"label": LABEL_ORDER},
        template=PLOTLY_TEMPLATE,
        title=title,
        color_discrete_sequence=[GREEN],
    )
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray",
                  annotation_text="50%", annotation_position="right")
    fig.update_layout(
        xaxis_title="Horizon",
        yaxis_title="% Positive",
        yaxis_tickformat=".0%",
        yaxis_range=[0, 1],
        font=PLOTLY_FONT,
    )
    return fig


def grouped_bar(long_df, x_col, y_col, color_col, title, y_fmt=".1%"):
    fig = px.bar(
        long_df.dropna(subset=[y_col]),
        x=x_col, y=y_col,
        color=color_col,
        barmode="group",
        category_orders={"label": LABEL_ORDER},
        template=PLOTLY_TEMPLATE,
        title=title,
        color_discrete_sequence=MAVEN_COLORS,
    )
    fig.update_layout(
        xaxis_title="Horizon",
        yaxis_title="Mean Return",
        yaxis_tickformat=y_fmt,
        hovermode="x unified",
        font=PLOTLY_FONT,
    )
    return fig


def sector_heatmap(df_all, min_n=1):
    """Heatmap: rows=sectors, cols=horizons, values=mean return."""
    sectors = sorted(df_all["Sector"].dropna().unique())
    data = []
    for s in sectors:
        sdf = df_all[df_all["Sector"] == s]
        row = [s]
        for h in HORIZON_COLS:
            vals = sdf[h].dropna()
            n    = len(vals)
            row.append(vals.mean() if n >= min_n else np.nan)
        data.append(row)

    cols  = ["Sector"] + [HORIZON_LABELS[h] for h in HORIZON_COLS]
    hm_df = pd.DataFrame(data, columns=cols).set_index("Sector")

    fig = go.Figure(go.Heatmap(
        z=hm_df.values * 100,  # percentage
        x=hm_df.columns.tolist(),
        y=hm_df.index.tolist(),
        colorscale=[
            [0.0, "#c0392b"], [0.4, "#f5f5f5"], [0.5, "#f5f5f5"],
            [0.6, "#f5f5f5"], [1.0, GREEN]
        ],
        zmid=0,
        text=np.where(
            np.isnan(hm_df.values),
            "n/a",
            [[f"{v:.1f}%" for v in row] for row in hm_df.values * 100]
        ),
        texttemplate="%{text}",
        hovertemplate="Sector: %{y}<br>Horizon: %{x}<br>Return: %{z:.2f}%<extra></extra>",
    ))
    fig.update_layout(
        title="Mean Return by Sector and Horizon",
        template=PLOTLY_TEMPLATE,
        height=400 + len(sectors) * 25,
        font=PLOTLY_FONT,
    )
    return fig


def deal_trajectory_chart(row):
    """Line chart for a single deal's return trajectory."""
    x, y = [], []
    for h in HORIZON_COLS:
        val = row.get(h)
        if not pd.isna(val):
            x.append(HORIZON_LABELS[h])
            y.append(val)
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers",
                               line=dict(color=NAVY, width=2),
                               marker=dict(color=GREEN, size=8)))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title=f"{row.get('Issuer', 'Deal')} ({row.get('Ticker', '')})",
        xaxis_title="Horizon",
        yaxis_title="Return vs Offer Price",
        yaxis_tickformat=".1%",
        template=PLOTLY_TEMPLATE,
        font=PLOTLY_FONT,
    )
    return fig


# ---------------------------------------------------------------------------
# Format helpers
# ---------------------------------------------------------------------------
def fmt_pct(x):
    return f"{x:.1%}" if not pd.isna(x) else "—"

def fmt_f(x, d=2):
    return f"{x:.{d}f}" if not pd.isna(x) else "—"

def color_return(val):
    if pd.isna(val): return ""
    c = "#c8f7c5" if val > 0 else "#f7c8c8"
    return f"background-color: {c}"


def style_metrics_table(mdf):
    """Style a metrics DataFrame for display."""
    disp = mdf.copy()
    disp["mean"]    = disp["mean"].map(lambda x: fmt_pct(x))
    disp["median"]  = disp["median"].map(lambda x: fmt_pct(x))
    disp["pct_pos"] = disp["pct_pos"].map(lambda x: fmt_pct(x))
    disp["std"]     = disp["std"].map(lambda x: fmt_pct(x))
    disp["sharpe"]  = disp["sharpe"].map(lambda x: fmt_f(x))
    disp["n"]       = disp["n"].astype(int)
    disp = disp.rename(columns={
        "label": "Horizon", "mean": "Mean Return", "median": "Median Return",
        "pct_pos": "% Positive", "std": "Std Dev", "sharpe": "Sharpe Ratio", "n": "N"
    })
    return disp[["Horizon", "Mean Return", "Median Return", "% Positive", "Std Dev", "Sharpe Ratio", "N"]]


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
def sidebar_filters(df):
    regions  = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    sectors  = ["All"] + sorted(df["Sector"].dropna().unique().tolist())
    sizes    = ["All"] + [s for s in DEAL_SIZE_ORDER if s in df["Deal Size Bucket"].unique()]
    mcaps    = ["All"] + [m for m in MCAP_ORDER       if m in df["MktCap Bucket"].unique()]
    years    = ["All"] + sorted(df["Year"].unique().tolist())
    types    = ["All"] + sorted(df["Type"].dropna().unique().tolist())

    sel_region  = st.sidebar.multiselect("Region",     regions,  default=["All"])
    sel_sector  = st.sidebar.multiselect("Sector",     sectors,  default=["All"])
    sel_size    = st.sidebar.multiselect("Deal Size",  sizes,    default=["All"])
    sel_mcap    = st.sidebar.multiselect("Market Cap", mcaps,    default=["All"])
    sel_year    = st.sidebar.multiselect("Year",       years,    default=["All"])
    sel_type    = st.sidebar.multiselect("Deal Type",  types,    default=["All"])
    min_n       = st.sidebar.slider("Min deals for breakdowns", 1, 20, 5)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Data:** CMG North Asia FOs, 2022–YTD 2026  \n"
        "**Returns:** vs local-currency offer price  \n"
        "**Horizons:** trading days post-pricing"
    )

    def _apply(fdf, sel, col):
        if "All" in sel or not sel:
            return fdf
        return fdf[fdf[col].isin(sel)]

    fdf = df.copy()
    fdf = _apply(fdf, sel_region, "Region")
    fdf = _apply(fdf, sel_sector, "Sector")
    fdf = _apply(fdf, sel_size,   "Deal Size Bucket")
    fdf = _apply(fdf, sel_mcap,   "MktCap Bucket")
    fdf = _apply(fdf, sel_year,   "Year")
    fdf = _apply(fdf, sel_type,   "Type")

    return fdf, min_n


# ---------------------------------------------------------------------------
# Tab 1: Summary
# ---------------------------------------------------------------------------
def tab_summary(df):
    ret_cols = HORIZON_COLS
    has_data = df[ret_cols].notna().any(axis=1)
    total_n      = len(df)
    pct_data     = has_data.sum() / total_n if total_n > 0 else 0
    date_min     = df["Pricing Date"].min().strftime("%b %Y")
    date_max     = df["Pricing Date"].max().strftime("%b %Y")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Deals",       f"{total_n:,}")
    c2.metric("Date Range",        f"{date_min} – {date_max}")
    c3.metric("Valid Price Data",  f"{pct_data:.0%} ({has_data.sum():,})")
    c4.metric("Regions Covered",   df["Region"].nunique())

    st.markdown("---")

    mdf = compute_metrics(df)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            mean_return_line(mdf, "Mean Return by Horizon (All Deals)"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            pct_positive_bar(mdf, "% of Deals Positive at Each Horizon"),
            use_container_width=True,
        )

    st.markdown("#### Summary Statistics — All Deals")
    disp = style_metrics_table(mdf)
    st.dataframe(disp, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Key Observations")
    # Auto-generate observations based on data
    valid_mdf = mdf.dropna(subset=["mean"])
    if len(valid_mdf) > 0:
        best_mean_row   = valid_mdf.loc[valid_mdf["mean"].idxmax()]
        best_sharpe_row = valid_mdf.dropna(subset=["sharpe"]).loc[valid_mdf.dropna(subset=["sharpe"])["sharpe"].idxmax()]
        obs = [
            f"**Best mean return** is at **{best_mean_row['label']}** "
            f"({best_mean_row['mean']:.1%} mean, {best_mean_row['pct_pos']:.0%} deals positive, n={int(best_mean_row['n'])})",
            f"**Best risk-adjusted return (Sharpe)** is at **{best_sharpe_row['label']}** "
            f"(ratio {best_sharpe_row['sharpe']:.2f})",
            f"Day 1 open return (immediate flip): {mdf.loc[mdf['label']=='D1 Open','mean'].values[0]:.2%} mean",
        ]
        for o in obs:
            st.markdown(f"- {o}")
    else:
        st.info("Run `fetch_prices.py` first to populate price data.")


# ---------------------------------------------------------------------------
# Tab 2: By Region
# ---------------------------------------------------------------------------
def tab_region(df):
    rmet = compute_metrics(df, groupby="Region")
    long_df = metrics_dict_to_df(rmet)
    long_df["label"] = long_df["horizon"].map(HORIZON_LABELS)

    st.plotly_chart(
        mean_return_line(long_df, "Mean Return by Horizon — By Region", color_col="group"),
        use_container_width=True,
    )

    fig_bar = grouped_bar(long_df, "label", "mean", "group",
                          "Mean Return by Region at Each Horizon")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Region × Horizon — Full Metrics")
    for region, mdf in rmet.items():
        with st.expander(f"**{region}** (n deals varies by horizon)", expanded=False):
            st.dataframe(style_metrics_table(mdf), use_container_width=True, hide_index=True)

    # Compact combined table
    combined = long_df.copy()
    combined["mean_fmt"]   = combined["mean"].map(fmt_pct)
    combined["pct_pos_fmt"]= combined["pct_pos"].map(fmt_pct)
    combined["n"]          = combined["n"].fillna(0).astype(int)
    pivot_mean = combined.pivot(index="label", columns="group", values="mean_fmt")
    pivot_mean.index.name = "Horizon"
    st.markdown("#### Mean Return by Region (compact pivot)")
    st.dataframe(pivot_mean, use_container_width=True)


# ---------------------------------------------------------------------------
# Tab 3: By Sector
# ---------------------------------------------------------------------------
def tab_sector(df, min_n):
    st.plotly_chart(sector_heatmap(df, min_n=min_n), use_container_width=True)

    all_sectors = sorted(df["Sector"].dropna().unique().tolist())
    sel_sector  = st.selectbox("Select sector for detail chart", all_sectors)
    sdf  = df[df["Sector"] == sel_sector]
    smdf = compute_metrics(sdf)
    n_total = len(sdf)
    if n_total < 10:
        st.warning(f"⚠️ Only {n_total} deals in {sel_sector} — interpret with caution.")
    st.plotly_chart(
        mean_return_line(smdf, f"Return Profile — {sel_sector} (n={n_total})"),
        use_container_width=True,
    )

    st.markdown("#### Sector × Horizon — Full Metrics")
    smet = compute_metrics(df, groupby="Sector")
    rows = []
    for sector, mdf in sorted(smet.items()):
        for _, r in mdf.iterrows():
            rows.append({
                "Sector":   sector,
                "Horizon":  r["label"],
                "Mean":     fmt_pct(r["mean"]),
                "Median":   fmt_pct(r["median"]),
                "% Pos":    fmt_pct(r["pct_pos"]),
                "Std":      fmt_pct(r["std"]),
                "Sharpe":   fmt_f(r["sharpe"]),
                "N":        int(r["n"]),
                "Flag":     "⚠️ Low N" if r["n"] < 10 else "",
            })
    tbl = pd.DataFrame(rows)
    st.dataframe(tbl, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Tab 4: By Deal Characteristics
# ---------------------------------------------------------------------------
def tab_characteristics(df):
    st.markdown("### Deal Size vs Market Cap")
    col1, col2 = st.columns(2)

    with col1:
        size_met = compute_metrics(df, groupby="Deal Size Bucket")
        size_long = metrics_dict_to_df(size_met)
        size_long["label"] = size_long["horizon"].map(HORIZON_LABELS)
        size_long["group"] = pd.Categorical(size_long["group"], categories=DEAL_SIZE_ORDER, ordered=True)
        fig = mean_return_line(size_long, "Mean Return by Deal Size", color_col="group")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        mcap_met  = compute_metrics(df, groupby="MktCap Bucket")
        mcap_long = metrics_dict_to_df(mcap_met)
        mcap_long["label"] = mcap_long["horizon"].map(HORIZON_LABELS)
        mcap_long["group"] = pd.Categorical(mcap_long["group"], categories=MCAP_ORDER, ordered=True)
        fig = mean_return_line(mcap_long, "Mean Return by Market Cap", color_col="group")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### By Year — Is the pattern changing over time?")
    year_met  = compute_metrics(df, groupby="Year")
    year_long = metrics_dict_to_df(year_met)
    year_long["label"] = year_long["horizon"].map(HORIZON_LABELS)
    year_long = year_long.sort_values("group")
    fig = mean_return_line(year_long, "Mean Return by Year", color_col="group")
    st.plotly_chart(fig, use_container_width=True)

    # Year pct positive bar
    pivot_pp = year_long.pivot(index="label", columns="group", values="pct_pos")
    pivot_pp.index = pd.Categorical(pivot_pp.index, categories=LABEL_ORDER, ordered=True)
    pivot_pp = pivot_pp.sort_index()

    fig2 = go.Figure()
    for yr, colour in zip(sorted(pivot_pp.columns), MAVEN_COLORS):
        fig2.add_trace(go.Bar(name=str(yr), x=pivot_pp.index.tolist(),
                              y=pivot_pp[yr], marker_color=colour))
    fig2.update_layout(
        barmode="group",
        title="% Deals Positive at Each Horizon — by Year",
        xaxis_title="Horizon", yaxis_title="% Positive",
        yaxis_tickformat=".0%", yaxis_range=[0, 1],
        template=PLOTLY_TEMPLATE,
        font=PLOTLY_FONT,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### Marketed FO vs Overnight FO")
    type_met  = compute_metrics(df, groupby="Type")
    type_long = metrics_dict_to_df(type_met)
    type_long["label"] = type_long["horizon"].map(HORIZON_LABELS)
    fig = mean_return_line(type_long, "Mean Return: Marketed vs Overnight FO", color_col="group")
    st.plotly_chart(fig, use_container_width=True)
    fig_bar = grouped_bar(type_long, "label", "mean", "group",
                          "Marketed vs Overnight — Mean Return at Each Horizon")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Deal Type — Full Metrics")
    for dtype, mdf in type_met.items():
        with st.expander(f"**{dtype}**", expanded=False):
            st.dataframe(style_metrics_table(mdf), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Pricing Discount vs Subsequent Return")
    _discount_analysis(df)


def _discount_analysis(df):
    """Show how pricing discount relates to subsequent returns."""
    disc_col = "Pricing Discount - To Last Trade"
    if disc_col not in df.columns:
        st.info("No discount column found.")
        return

    valid = df[[disc_col] + HORIZON_COLS].dropna(subset=[disc_col])
    if len(valid) < 20:
        st.info("Insufficient data for discount analysis.")
        return

    valid = valid.copy()
    try:
        valid["Discount Quartile"] = pd.qcut(
            valid[disc_col], q=4,
            labels=["Q1 (Least Disc.)", "Q2", "Q3", "Q4 (Most Disc.)"],
        )
    except ValueError:
        st.info("Could not create discount quartiles (insufficient spread).")
        return

    qmet = {}
    for q in ["Q1 (Least Disc.)", "Q2", "Q3", "Q4 (Most Disc.)"]:
        qdf = valid[valid["Discount Quartile"] == q]
        if len(qdf) == 0:
            continue
        rows = []
        for h in HORIZON_COLS:
            vals = qdf[h].dropna()
            rows.append(dict(
                horizon=h, label=HORIZON_LABELS[h],
                mean=vals.mean() if len(vals) > 0 else np.nan, n=len(vals),
            ))
        qmet[q] = pd.DataFrame(rows)

    long_df = metrics_dict_to_df(qmet)
    long_df["label"] = long_df["horizon"].map(HORIZON_LABELS)
    fig = mean_return_line(long_df, "Mean Return by Pricing Discount Quartile", color_col="group")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Q4 = deepest discount deals (most negative Pricing Discount - To Last Trade). "
               "These are typically priced at the steepest discount to current market price.")


# ---------------------------------------------------------------------------
# Tab 5: Deal Explorer
# ---------------------------------------------------------------------------
def tab_explorer(df):
    st.markdown("### Individual Deal Browser")

    # Build display table
    display_cols = [
        "Pricing Date", "Issuer", "Ticker", "Region", "Sector",
        "Deal Size $M", "MktCap $B", "Type",
        "Pricing Discount - To Last Trade",
    ] + HORIZON_COLS

    disp = df[display_cols].copy()
    disp["Pricing Date"] = disp["Pricing Date"].dt.strftime("%Y-%m-%d")
    disp = disp.rename(columns={
        **HORIZON_LABELS,
        "Pricing Discount - To Last Trade": "Discount %",
    })
    disp["Discount %"] = (disp["Discount %"] * 100).round(2)

    horizon_display = list(HORIZON_LABELS.values())

    # Search box
    search = st.text_input("Search issuer or ticker", "")
    if search:
        mask = (
            disp["Issuer"].str.contains(search, case=False, na=False) |
            disp["Ticker"].str.contains(search, case=False, na=False)
        )
        disp = disp[mask]

    st.caption(f"Showing {len(disp):,} deals. Click a row to see its return trajectory.")

    # Color-coded return columns using Styler
    def _color(val):
        if isinstance(val, float) and not pd.isna(val):
            c = "#c8f7c5" if val > 0 else "#f7c8c8"
            return f"background-color: {c}"
        return ""

    ret_display_cols = [c for c in disp.columns if c in horizon_display]

    # Format return columns
    disp_fmt = disp.copy()
    for c in ret_display_cols:
        disp_fmt[c] = disp_fmt[c].map(lambda x: f"{x:.1%}" if not pd.isna(x) else "—")

    st.dataframe(disp_fmt, use_container_width=True, hide_index=True, height=400)

    # Individual deal chart
    st.markdown("#### Deal Return Trajectory")
    issuers = df["Issuer"].dropna().unique().tolist()
    sel = st.selectbox("Select a deal (issuer)", sorted(issuers))
    if sel:
        rows = df[df["Issuer"] == sel]
        if len(rows) > 1:
            idx = st.selectbox(
                "Multiple deals found — select by date",
                rows["Pricing Date"].dt.strftime("%Y-%m-%d").tolist(),
            )
            row = rows[rows["Pricing Date"].dt.strftime("%Y-%m-%d") == idx].iloc[0]
        else:
            row = rows.iloc[0]
        st.plotly_chart(deal_trajectory_chart(row), use_container_width=True)
        meta = {
            "Issuer": row["Issuer"], "Ticker": row["Ticker"],
            "Region": row["Region"], "Sector": row["Sector"],
            "Pricing Date": row["Pricing Date"].strftime("%Y-%m-%d"),
            "Offer Price": f"{row['Offer Price']:,.2f} {row['Currency']}",
            "Deal Size": f"${row['Deal Size $M']:,.1f}M",
            "Type": row["Type"],
            "Discount to Last Trade": fmt_pct(row["Pricing Discount - To Last Trade"]),
        }
        st.json(meta)

    st.markdown("---")
    st.markdown("#### Deals with Missing Price Data")
    missing = df[df[HORIZON_COLS].isna().all(axis=1)][
        ["Pricing Date", "Issuer", "Ticker", "Region", "yf_ticker"]
    ].copy()
    missing["Pricing Date"] = missing["Pricing Date"].dt.strftime("%Y-%m-%d")
    if len(missing) > 0:
        st.dataframe(missing, use_container_width=True, hide_index=True)
        st.caption(f"{len(missing)} deals with no price data (likely delisted, recently listed, or ticker mismatch)")
    else:
        st.success("All deals have at least some price data.")


# ---------------------------------------------------------------------------
# Interaction analyses helpers (used across tabs)
# ---------------------------------------------------------------------------
def tab_interactions(df, min_n):
    st.markdown("### Region × Deal Type")
    sub = df.dropna(subset=["Region", "Type"])
    sub["Group"] = sub["Region"] + " | " + sub["Type"]
    gmet  = compute_metrics(sub, groupby="Group")
    glong = metrics_dict_to_df(gmet)
    glong["label"] = glong["horizon"].map(HORIZON_LABELS)
    glong = glong[glong["n"] >= min_n]
    if len(glong) > 0:
        fig = mean_return_line(glong, "Region × Deal Type — Mean Return", color_col="group")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data with current min-N filter.")

    st.markdown("### Region × Sector (best horizons)")
    # Show a table: for each region-sector combo, which horizon maximises mean return?
    combos = []
    for region in sub["Region"].unique():
        for sector in sub["Sector"].unique():
            sdf = df[(df["Region"] == region) & (df["Sector"] == sector)]
            valid_rets = {h: sdf[h].dropna() for h in HORIZON_COLS}
            if all(len(v) < min_n for v in valid_rets.values()):
                continue
            means = {h: v.mean() for h, v in valid_rets.items() if len(v) >= min_n}
            if not means:
                continue
            best_h = max(means, key=means.get)
            combos.append({
                "Region": region, "Sector": sector,
                "Best Horizon": HORIZON_LABELS[best_h],
                "Mean Return": fmt_pct(means[best_h]),
                "N": len(valid_rets[best_h]),
            })
    if combos:
        st.dataframe(pd.DataFrame(combos), use_container_width=True, hide_index=True)
    else:
        st.info("No region × sector combinations meet the minimum deal threshold.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    logo_b64 = _logo_b64()

    # ------------------------------------------------------------------
    # Global CSS — Times New Roman, Maven navy/green brand
    # ------------------------------------------------------------------
    st.markdown(f"""
    <style>
    /* ---- Typography ---- */
    html, body, [class*="css"], .stApp, .stMarkdown,
    .stTextInput, .stSelectbox, .stMultiSelect, .stSlider,
    button, input, label, p, span, div {{
        font-family: 'Times New Roman', Times, serif !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Times New Roman', Times, serif !important;
        color: #1a3a5c !important;
        letter-spacing: 0.02em;
    }}

    /* ---- Page background ---- */
    .stApp {{ background: #ffffff; }}

    /* ---- Header banner ---- */
    .maven-header {{
        display: flex;
        align-items: center;
        background: #0d1f2d;
        padding: 18px 32px;
        margin: -1rem -1rem 1.5rem -1rem;
        border-bottom: 3px solid #2e7d4f;
    }}
    .maven-header img {{
        height: 52px;
        margin-right: 28px;
    }}
    .maven-header-text {{
        display: flex;
        flex-direction: column;
    }}
    .maven-header-title {{
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
        letter-spacing: 0.04em;
    }}
    .maven-header-sub {{
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 0.82rem;
        color: #a8d5b5;
        margin-top: 4px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}
    .maven-divider {{
        border: none;
        border-top: 1px solid #d0dde8;
        margin: 0.5rem 0 1.2rem 0;
    }}

    /* ---- Metric cards ---- */
    [data-testid="metric-container"] {{
        background: #f7fbf9;
        border: 1px solid #2e7d4f;
        border-radius: 4px;
        padding: 14px 18px;
    }}
    [data-testid="metric-container"] label {{
        color: #1a3a5c !important;
        font-weight: 600;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    [data-testid="metric-container"] [data-testid="metric-value"] {{
        color: #1a3a5c !important;
        font-size: 1.5rem !important;
    }}

    /* ---- Tabs ---- */
    div[data-testid="stTabs"] button {{
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 1.05rem;
        font-weight: 700;
        color: #4a6278;
        letter-spacing: 0.03em;
        padding: 8px 20px;
        border-radius: 0;
        border-bottom: 2px solid transparent;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        border-bottom: 2px solid #2e7d4f !important;
        color: #1a3a5c !important;
    }}
    div[data-testid="stTabs"] button:hover {{
        color: #1a3a5c !important;
        background: #f0f6f2 !important;
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: #0d1f2d !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #d6e8f0 !important;
        font-family: 'Times New Roman', Times, serif !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #ffffff !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p {{
        color: #a8d5b5 !important;
        font-size: 0.82rem;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: #2e7d4f;
        opacity: 0.5;
    }}

    /* ---- Dataframe ---- */
    [data-testid="stDataFrame"] th {{
        background: #1a3a5c !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
    }}

    /* ---- Info/warning boxes ---- */
    .stAlert {{ border-radius: 4px; }}

    /* ---- Permanently visible sidebar — hide collapse/expand toggles ---- */
    [data-testid="collapsedControl"] {{ display: none !important; }}
    button[data-testid="stBaseButton-header"] {{ display: none !important; }}
    [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
    section[data-testid="stSidebar"] > div:first-child > button {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Header banner (logo + title)
    # ------------------------------------------------------------------
    st.markdown(f"""
    <div class="maven-header">
        <img src="data:image/png;base64,{logo_b64}" alt="" title="" draggable="false" style="pointer-events:none;">
        <div class="maven-header-text">
            <div class="maven-header-title">North Asia Follow-On Offering — Unwind Analysis</div>
            <div class="maven-header-sub">Sky Lee &nbsp;|&nbsp; HK / China &nbsp;&bull;&nbsp; Japan &nbsp;&bull;&nbsp; Korea &nbsp;|&nbsp; 2022 – YTD 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    master, has_prices = load_master()

    if not has_prices:
        st.warning(
            "Price data not found. Run `python3 fetch_prices.py` from the project "
            "directory to build the returns cache, then restart the app."
        )

    # Sidebar — logo + filters
    st.sidebar.markdown(
        f'<div style="text-align:center; padding: 12px 8px 4px 8px;">'
        f'<img src="data:image/png;base64,{logo_b64}" alt="" title="" draggable="false" style="width:85%; opacity:0.92; pointer-events:none;">'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<hr style="border-color:#2e7d4f; margin: 8px 0 14px 0;">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<p style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; '
        'color:#7ba8c4 !important; margin-bottom:6px;">Filters</p>',
        unsafe_allow_html=True,
    )

    filtered, min_n = sidebar_filters(master)
    if len(filtered) == 0:
        st.warning("No deals match the current filters. Please broaden your selection.")
        return

    # Tabs — no emojis
    tabs = st.tabs([
        "Summary",
        "By Region",
        "By Sector",
        "Deal Characteristics",
        "Deal Explorer",
        "Interaction Analysis",
    ])

    with tabs[0]:
        tab_summary(filtered)
    with tabs[1]:
        tab_region(filtered)
    with tabs[2]:
        tab_sector(filtered, min_n)
    with tabs[3]:
        tab_characteristics(filtered)
    with tabs[4]:
        tab_explorer(filtered)
    with tabs[5]:
        tab_interactions(filtered, min_n)


if __name__ == "__main__":
    main()
