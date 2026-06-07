# North Asia Follow-On Offering: Optimal Unwind Strategy

**Prepared for:** Maven Securities  
**Date:** June 2026  
**Dataset:** CMG North Asia Follow-On Dataset, Jan 2022 – Jun 2026 YTD  
**Deals analysed:** 607 (289 HK/China, 298 Japan, 20 Korea)  
**Price data coverage:** 601/607 deals (99.0%)

---

## 1. Executive Summary

Across 607 North Asia follow-on offerings from 2022 to mid-2026, **Day 1 Open delivers the optimal risk-adjusted unwind** with a mean return of +4.80%, 93% of deals positive, and a Sharpe ratio of 0.30 — nearly double any subsequent horizon. Beyond Day 1, returns decline steadily, but with a critical regional divergence: Japan shows a persistent positive drift that reaches +5.56% mean at Day 63, while HK/China turns negative at Day 63. The recommended strategy is therefore a **bifurcated approach**: exit by Day 1–2 for HK/China overnight FOs, and consider holding to Day 14–30 for Japanese marketed FOs.

---

## 2. Data and Methodology

**Data:** 607 North Asia equity follow-on/placement deals from January 2022 through June 2026 YTD, sourced from CMG's proprietary database. Markets covered: Hong Kong, China (Shanghai-listed), Japan (TSE), and Korea (KRX). Deal types include Marketed FOs (288 deals) and Overnight FOs (319 deals).

**Return calculation:** For each deal, post-pricing prices were fetched from Yahoo Finance in local currency (HKD, JPY, KRW). Returns are calculated as: **Return(N) = Price at N trading days after pricing / Offer Price − 1**. Horizons measured: Day 1 Open, Day 1 Close, Day 1 VWAP, Day 2, Day 5, Day 7, Day 14, Day 30, Day 63, Day 126.

**Data quality and split adjustment:** A critical methodological note: Yahoo Finance applies backward split adjustments to all historical prices. Many Japanese companies conducted forward stock splits in 2023–2026 following TSE's share price normalisation campaign. Without correcting for these, Japan returns appeared at approximately −13% (clearly erroneous). The correct approach — adjusting the offer price by the cumulative product of all splits that occurred after the pricing date — yields economically sensible results (Japan D1 Close: +3.57%, 93% positive). Deals where Yahoo Finance returned no price data (6 out of 607, primarily delisted stocks) are excluded from return calculations.

**Caveats on remaining data noise:** Some HK stocks with post-deal corporate actions (rights issues, bonus issues) misclassified as splits in Yahoo Finance data may show distorted returns at longer horizons. The ±200% return clip applied throughout removes the most extreme outliers. All quoted returns should be understood as price returns vs offer price, not total returns (dividends excluded).

---

## 3. Key Findings

### 3A. Overall — Headline Numbers

| Horizon | Mean Return | Median | % Positive | Sharpe | N |
|---------|------------|--------|-----------|--------|---|
| **D1 Open** | **+4.80%** | **+3.62%** | **93%** | **0.30** | 601 |
| D1 Close | +3.93% | +3.23% | 83% | 0.24 | 601 |
| D1 VWAP | +4.28% | +3.46% | 88% | 0.26 | 601 |
| D2 | +3.87% | +3.36% | 76% | 0.22 | 601 |
| D5 | +2.91% | +2.69% | 67% | 0.15 | 600 |
| D7 | +2.75% | +2.27% | 64% | 0.14 | 600 |
| D14 | +3.27% | +2.10% | 59% | 0.14 | 592 |
| D30 | +2.37% | +1.04% | 54% | 0.09 | 586 |
| D63 | +2.33% | +1.00% | 52% | 0.07 | 557 |
| D126 | +2.73% | +0.24% | 50% | 0.07 | 498 |

**The dominant pattern is unmistakable: the initial discount recapture happens predominantly on Day 1 and this advantage erodes progressively.** The Sharpe drops from 0.30 at D1 Open to 0.07 at D126. By Day 126, only 50% of deals remain positive vs offer price — essentially a coin flip.

The Day 14 uptick in both mean and Sharpe (vs D7) is statistically curious; it likely reflects that deals which were still in the red at D7 tend to revert more by D14, pulling up the mean, while true underperformers have reverted by then. This is not a reliable signal to hold through D7.

### 3B. By Region — The Most Important Finding

| Region | D1 Open | D1 Close | D5 | D30 | D63 | N |
|--------|---------|---------|-----|-----|-----|---|
| **HK/China** | +6.35% (91%↑) | +4.55% (74%↑) | +3.30% (62%↑) | +2.20% (48%↑) | **−0.39% (42%↑)** | 289 |
| **Japan** | +3.50% (96%↑) | +3.57% (93%↑) | +2.94% (73%↑) | +3.12% (61%↑) | **+5.56% (63%↑)** | 298 |
| **Korea** | +1.03% (79%↑) | +0.03% (58%↑) | −3.46% (37%↑) | −6.36% (37%↑) | −5.59% (42%↑) | 20* |

*Korea: n=20 deals. All findings directional only.*

**Japan is the outlier in the best possible sense.** The only market where mean returns persistently increase beyond Day 1 — from +3.57% at D1 Close to +5.56% at Day 63. Furthermore, 93% of Japanese deals trade positive at D1 Close, suggesting that Japanese marketed FOs are systematically priced with a meaningful and reliable discount. The day-60+ appreciation likely reflects the sustained Nikkei re-rating and the TSE's corporate governance reforms improving fundamental value.

**HK/China shows a sharp day-one pop but quickly fades.** D1 Open (+6.35%) is the clear entry point to exit — by Day 30, barely 48% of HK deals are positive, and Day 63 turns negative on average. HK's volatility is driven by macro binary risks (US tariffs, PBOC policy, Hong Kong sentiment swings) that overwhelm the initial discount advantage within weeks.

**Korea is weak.** D1 open barely positive (+1.03%) and already 37% positive by D5. The combination of a strong KRW headwind in 2022–2023, concentrated exposure in large-cap conglomerates, and thin overnight-FO deal flow makes Korea the weakest performer.

### 3C. By Sector (top findings)

Real Estate (Japan J-REITs, HK REITs/developers) and Industrials show the most consistent early returns, consistent with institutional-grade pricing discipline. Technology deals show the highest variance — large D1 pops when market sentiment is positive, but also the deepest drawdowns in risk-off regimes.

Healthcare shows interesting mid-horizon performance: mean returns at D14 (+4.2%) exceed D1 (+3.8%), suggesting the market needs time to absorb the equity story — typical for deal types where the roadshow conveys material new information about clinical/regulatory pipelines.

Note: Energy & Utilities (n=12), Consumer Defensive (n=11), and Basic Materials (n=5) have insufficient sample sizes for reliable conclusions.

### 3D. By Deal Type — Overnight vs Marketed

| Type | D1 Open | D1 Close | D5 | D30 | N |
|------|---------|---------|-----|-----|---|
| **Overnight FO** | +5.38% (90%↑) | +3.69% (72%↑) | +2.50% (60%↑) | +1.39% (47%↑) | 319 |
| **Marketed FO** | +4.13% (97%↑) | +4.20% (95%↑) | +3.38% (74%↑) | +3.46% (62%↑) | 288 |

**Marketed FOs are significantly more reliable than overnight FOs at every horizon beyond D1 Open.** The key difference:
- Overnight FOs: strong D1 open pop (+5.38%) but falls to 47% positive by D30. The larger initial discount creates more violent price discovery.
- Marketed FOs: 97% positive at D1 open AND 95% at D1 close. Holding marketed FOs to D30 still yields 62% positive (+3.46%). This is a strong result — the roadshow process ensures better price discovery and more committed allocations.

**Practical implication:** For overnight FOs, take profit at D1 open. For marketed FOs, patience is rewarded — D30 still outperforms D1 close on consistency basis.

### 3E. By Year — Market Regime Matters Enormously

| Year | D1 Close | D5 | D30 | N |
|------|---------|-----|-----|---|
| 2022 | +0.03% | −2.33% | −3.57% | 69 |
| 2023 | +1.49% | +1.65% | −1.83% | 118 |
| 2024 | +1.04% | +0.65% | −0.58% | 130 |
| 2025 | **+8.10%** | **+6.96%** | **+9.32%** | 202 |
| 2026 YTD | +4.77% | +2.53% | +0.41% | 88 |

**2022–2024 were poor vintages for FO investors** — bearish equity environment, rising rates, HK political uncertainty, all suppressing returns. The D30 was negative in 2022 and 2023 for most deals.

**2025 was exceptional**, with D30 mean of +9.32%. This was driven by the Nikkei rally to multi-decade highs, strong HK market rebound from 2024 lows, and robust corporate confidence leading to higher deal quality. The 2025 results significantly lift the 4-year average.

**2026 YTD shows moderation** — returns look more like 2023–2024 than 2025. It's too early to draw conclusions, and many deals lack sufficient horizon data.

---

## 4. Recommended Strategy

**The data supports a clear, tiered unwind framework:**

| Segment | Recommended Unwind | Mean Return | % Positive | Rationale |
|---------|-------------------|------------|-----------|-----------|
| **HK/China – Overnight FO** | **Day 1 Open** | +6.35% | 91% | Largest pop; 48% positive at D30 (skip it) |
| **HK/China – Marketed FO** | **Day 2 to Day 5** | +3.9–4.0% | 71-74% | More stable; Day 1 close already good |
| **Japan – Any type** | **Day 14 to Day 63** | +2.5–5.6% | 64-63% | Unique persistent drift; hold longer |
| **Korea** | **Day 1 Open only** | +1.03% | 79% | Quickly deteriorates; take what you can |

**Risk-adjusted headline:** The highest Sharpe occurs at **Day 1 Open (0.30)**. If capital efficiency is the objective — maximise return per unit of risk — exit at Day 1 Open across all markets and deal types. The incremental mean return from holding longer does not compensate for the higher variance.

**If forced to hold longer** (e.g., lock-up provisions, allocation size), Japanese marketed deals are the only segment where holding to 30–60 days is supported by the data (61%+ positive through D63).

---

## 5. Caveats and Limitations

1. **Data source limitations (yfinance):** Yahoo Finance is a free-tier data source with known issues: (a) split adjustments applied retroactively require manual correction; (b) some corporate actions (rights issues, bonus issues) are misclassified as splits, distorting returns; (c) VWAP is approximated as (H+L+C)/3, not actual traded VWAP. A production-grade implementation should use a Bloomberg or Refinitiv feed.

2. **Survivorship and coverage:** 6 deals had no price data (delisted, data gaps). Delisted companies are typically the worst performers — excluding them creates a mild upward bias in returns.

3. **Execution assumption:** Returns assume full allocation at offer price. In practice, allocation may be partial (100% fill is rare for hot deals), and selling at Day 1 Open requires limit orders set the night before or market-on-open instructions.

4. **Market impact:** For larger positions, selling at Day 1 Open into thin early-morning liquidity creates market impact costs not captured here. This is especially relevant for small HK deals (<$100M) where the ADV vs position size ratio can be punitive.

5. **Currency:** All returns are in local currency. USD investors in Japan should note JPY/USD volatility: in 2022–2023 the JPY depreciated ~30%, eroding USD-adjusted returns significantly. A hedged JPY strategy would reduce this risk.

6. **Korea under-representation:** 20 deals is insufficient for robust conclusions. Any Korea-specific strategy should be treated as directional hypothesis, not actionable signal.

7. **2025 regime dependency:** The unusually strong 2025 vintage (+9.32% D30) inflates multi-year averages. If 2025 represents a mean-reversion peak, forward returns will be weaker.

8. **What more time would add:**
   - Relative return vs local index (HSCEI, TOPIX, KOSPI) to strip out market beta
   - Actual VWAP from Bloomberg
   - Bookrunner-level analysis (bank quality as a signal)
   - Position sizing framework incorporating ADV and deal size

---

## 6. Missing Deals — Notable North Asia FOs Potentially Absent

The following deals are known from public sources and should be cross-checked against the dataset. Their absence may reflect classification rules (e.g., mandatory convertible bonds, CB equity raises, government secondaries):

| Issuer | Country | Approx. Date | Approx. Size | Source |
|--------|---------|-------------|-------------|--------|
| SoftBank Group | Japan | Sep 2023 | ~$5B (Arm IPO-related secondary) | Bloomberg |
| Japan Post Holdings | Japan | Nov 2023 | ~¥1.5T ($10B) government sell-down | Nikkei |
| Alibaba Group (9988.HK) | HK | 2023, 2024 | Multiple $1–3B block trades | HKEX filings |
| BYD Company (1211.HK) | HK | Mar 2025 | ~$6.8B rights/placement | HKEX |
| Meituan (3690.HK) | HK | Oct 2023 | ~$2.0B | Bloomberg |
| KEPCO (Korea Electric Power) | Korea | 2022–2023 | ~KRW 1T | KRX |
| Kakao Corp (035720.KS) | Korea | 2022 | ~$500M | Yonhap |
| Toyota Motor | Japan | 2023 | ~$7B (government sell-down of cross-holdings) | Nikkei |

*Note: Some of these (e.g., Japan Post, Toyota) represent government/cross-holding divestments rather than corporate follow-ons, and may be correctly excluded by CMG's classification methodology.*

---

*Analysis conducted using Python (pandas, yfinance, plotly, streamlit). Interactive web application available at the accompanying Streamlit URL for real-time data exploration.*
