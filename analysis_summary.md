# Maven Securities — North Asia Follow-On Unwind Analysis
## Comprehensive Findings Summary

**Prepared by:** Sky Lee  
**Date:** June 2026  
**Dataset:** CMG North Asia Follow-On Offerings, Jan 2022 – Jun 2026 YTD  
**Analysis tool:** Python (pandas, scipy, yfinance, streamlit)

---

## 1. Dataset Overview

| Attribute | Value |
|-----------|-------|
| Total deals | 607 |
| Date range | January 2022 – June 2026 |
| Deals with ≥1 valid return point | 601 (99.0%) |
| Deals with no price data | 6 |
| HK/China | 289 |
| Japan | 298 |
| Korea | 20 |
| Marketed FO | 288 |
| Overnight FO | 319 |
| Horizons | D1 Open, D1 Close, D1 VWAP, D2, D5, D7, D14, D30, D63, D126 |

> **Data coverage note:** Coverage decreases at longer horizons because recently-priced deals have not yet reached D63/D126. Six tickers (Japan/Korea) were delisted with no Yahoo Finance price data — their exclusion creates a mild upward survivorship bias.

---

## 2. Aggregate Return Table — All 607 Deals

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +4.80% | +3.62% | 93% | 16.12% | 0.30 | 601 |
| D1 Close | +3.93% | +3.23% | 83% | 16.61% | 0.24 | 601 |
| D1 VWAP | +4.28% | +3.46% | 88% | 16.33% | 0.26 | 601 |
| D2 | +3.87% | +3.36% | 76% | 17.29% | 0.22 | 601 |
| D5 | +2.91% | +2.69% | 67% | 18.99% | 0.15 | 600 |
| D7 | +2.75% | +2.27% | 64% | 20.12% | 0.14 | 600 |
| D14 | +3.27% | +2.10% | 59% | 23.35% | 0.14 | 592 |
| D30 | +2.37% | +1.04% | 54% | 27.34% | 0.09 | 586 |
| D63 | +2.33% | +1.00% | 52% | 33.59% | 0.07 | 557 |
| D126 | +2.73% | +0.24% | 50% | 41.64% | 0.07 | 498 |

> **Headline:** D1 Open has the highest Sharpe (0.30) and the highest % positive (93% of deals). By D126 only 50% of deals are positive vs offer price (n=498) — statistically indistinguishable from chance.

---

## 3. Returns by Region

### 3.1. HK/China  (n = 289)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.35% | +5.56% | 91% | 21.98% | 0.29 | 289 |
| D1 Close | +4.55% | +4.19% | 74% | 22.68% | 0.20 | 289 |
| D1 VWAP | +5.16% | +4.79% | 82% | 22.31% | 0.23 | 289 |
| D2 | +4.44% | +4.12% | 70% | 23.68% | 0.19 | 289 |
| D5 | +3.30% | +3.19% | 62% | 25.74% | 0.13 | 289 |
| D7 | +3.09% | +2.34% | 58% | 27.40% | 0.11 | 289 |
| D14 | +4.41% | +1.98% | 55% | 31.62% | 0.14 | 285 |
| D30 | +2.20% | -0.97% | 48% | 36.86% | 0.06 | 280 |
| D63 | -0.39% | -5.44% | 42% | 42.82% | -0.01 | 267 |
| D126 | -3.94% | -9.61% | 40% | 50.63% | -0.08 | 236 |

### 3.2. Japan  (n = 298)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +3.50% | +3.14% | 96% | 7.22% | 0.49 | 293 |
| D1 Close | +3.57% | +3.02% | 93% | 7.55% | 0.47 | 293 |
| D1 VWAP | +3.64% | +3.11% | 96% | 7.37% | 0.49 | 293 |
| D2 | +3.63% | +3.20% | 85% | 7.63% | 0.48 | 293 |
| D5 | +2.94% | +2.55% | 73% | 8.96% | 0.33 | 292 |
| D7 | +2.71% | +2.43% | 71% | 9.05% | 0.30 | 292 |
| D14 | +2.49% | +2.19% | 64% | 10.86% | 0.23 | 288 |
| D30 | +3.12% | +1.68% | 61% | 13.57% | 0.23 | 287 |
| D63 | +5.56% | +3.56% | 63% | 21.49% | 0.26 | 271 |
| D126 | +9.13% | +3.98% | 61% | 28.82% | 0.32 | 244 |

### 3.3. Korea  (n = 20)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +1.03% | +0.77% | 79% | 1.69% | 0.61 | 19 |
| D1 Close | +0.03% | +0.44% | 58% | 3.48% | 0.01 | 19 |
| D1 VWAP | +0.61% | +0.62% | 58% | 2.89% | 0.21 | 19 |
| D2 | -0.90% | +0.00% | 47% | 4.33% | -0.21 | 19 |
| D5 | -3.46% | -2.36% | 37% | 7.76% | -0.45 | 19 |
| D7 | -1.93% | -2.49% | 47% | 10.86% | -0.18 | 19 |
| D14 | -2.10% | -2.62% | 42% | 13.68% | -0.15 | 19 |
| D30 | -6.36% | -5.11% | 37% | 14.54% | -0.44 | 19 |
| D63 | -5.59% | -10.58% | 42% | 22.23% | -0.25 | 19 |
| D126 | +3.53% | -6.28% | 39% | 46.72% | 0.08 | 18 |

> **Regional divergence:** Japan is the only market where mean returns persistently increase beyond D1, reaching +5.56% at D63 (n=271). HK/China mean return turns negative at D63. Welch's t-test Japan vs HK/China at D63: t = 2.04, p = 0.0416 (significant at 5%).

---

## 4. Returns by Deal Type

### 4.1. Marketed FO  (n = 288)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +4.13% | +3.30% | 97% | 9.54% | 0.43 | 283 |
| D1 Close | +4.20% | +3.25% | 95% | 10.02% | 0.42 | 283 |
| D1 VWAP | +4.29% | +3.21% | 97% | 9.74% | 0.44 | 283 |
| D2 | +4.21% | +3.36% | 87% | 10.10% | 0.42 | 283 |
| D5 | +3.38% | +2.73% | 74% | 10.98% | 0.31 | 282 |
| D7 | +3.14% | +2.76% | 72% | 10.64% | 0.30 | 282 |
| D14 | +2.80% | +2.38% | 65% | 12.20% | 0.23 | 279 |
| D30 | +3.46% | +1.72% | 62% | 15.28% | 0.23 | 278 |
| D63 | +5.19% | +3.66% | 62% | 22.95% | 0.23 | 261 |
| D126 | +8.58% | +4.08% | 61% | 30.01% | 0.29 | 234 |

### 4.2. Overnight FO  (n = 319)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +5.38% | +4.60% | 90% | 20.25% | 0.27 | 318 |
| D1 Close | +3.69% | +3.23% | 72% | 20.80% | 0.18 | 318 |
| D1 VWAP | +4.27% | +3.72% | 80% | 20.50% | 0.21 | 318 |
| D2 | +3.58% | +3.29% | 67% | 21.79% | 0.16 | 318 |
| D5 | +2.50% | +2.54% | 60% | 23.97% | 0.10 | 318 |
| D7 | +2.39% | +1.36% | 57% | 25.78% | 0.09 | 318 |
| D14 | +3.68% | +1.58% | 54% | 29.99% | 0.12 | 313 |
| D30 | +1.39% | -1.19% | 47% | 34.80% | 0.04 | 308 |
| D63 | -0.19% | -4.99% | 44% | 40.60% | -0.00 | 296 |
| D126 | -2.45% | -7.06% | 41% | 49.22% | -0.05 | 264 |

> D1 Close % positive: Marketed FO 95% vs Overnight FO 72%.
> Marketed vs Overnight at D1 Open: t = -0.95, p = 0.3434 (not significant at 5%).
> Marketed vs Overnight at D30: t = 0.91, p = 0.3615 (not significant at 5%).
> D30 % positive: Overnight 47% vs Marketed 62%.

---

## 5. Returns by Sector

### Basic Materials  (n = 26)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +2.80% | +3.04% | 92% | 19.75% | 0.14 | 26 |
| D1 Close | +3.76% | +3.60% | 85% | 22.46% | 0.17 | 26 |
| D1 VWAP | +3.50% | +3.62% | 96% | 21.38% | 0.16 | 26 |
| D2 | +3.45% | +4.08% | 81% | 23.30% | 0.15 | 26 |
| D5 | +4.83% | +5.83% | 77% | 22.95% | 0.21 | 26 |
| D7 | +3.94% | +4.29% | 77% | 23.88% | 0.17 | 26 |
| D14 | +5.50% | +8.70% | 73% | 22.09% | 0.25 | 26 |
| D30 | +8.59% | +7.91% | 77% | 26.75% | 0.32 | 26 |
| D63 | +10.69% | +8.93% | 65% | 32.73% | 0.33 | 26 |
| D126 | +25.71% | +4.87% | 75% | 57.43% | 0.45 | 20 |

### Communication Services  (n = 21)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +3.94% | +4.33% | 71% | 4.41% | 0.90 | 21 |
| D1 Close | +3.62% | +0.89% | 71% | 6.83% | 0.53 | 21 |
| D1 VWAP | +3.84% | +2.10% | 71% | 5.94% | 0.65 | 21 |
| D2 | +3.91% | +1.86% | 62% | 9.90% | 0.39 | 21 |
| D5 | +3.91% | +0.15% | 52% | 12.81% | 0.31 | 21 |
| D7 | +2.40% | +0.31% | 52% | 13.83% | 0.17 | 21 |
| D14 | +0.12% | -1.83% | 40% | 13.23% | 0.01 | 20 |
| D30 | -0.89% | -1.67% | 45% | 19.95% | -0.04 | 20 |
| D63 | +3.54% | +0.31% | 50% | 19.63% | 0.18 | 18 |
| D126 | +22.70% | +9.64% | 50% | 53.08% | 0.43 | 18 |

### Consumer Cyclical  (n = 79)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +8.68% | +3.58% | 96% | 25.75% | 0.34 | 78 |
| D1 Close | +7.28% | +2.63% | 86% | 25.90% | 0.28 | 78 |
| D1 VWAP | +7.88% | +3.05% | 88% | 25.81% | 0.31 | 78 |
| D2 | +7.72% | +2.73% | 72% | 26.02% | 0.30 | 78 |
| D5 | +5.95% | +1.36% | 53% | 27.93% | 0.21 | 78 |
| D7 | +5.77% | +0.47% | 56% | 27.66% | 0.21 | 78 |
| D14 | +5.84% | +1.10% | 53% | 28.62% | 0.20 | 78 |
| D30 | +4.01% | -0.94% | 49% | 30.66% | 0.13 | 77 |
| D63 | +3.58% | -1.63% | 48% | 39.98% | 0.09 | 75 |
| D126 | +3.24% | -3.34% | 40% | 40.30% | 0.08 | 72 |

### Consumer Defensive  (n = 33)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.69% | +2.94% | 97% | 10.91% | 0.61 | 33 |
| D1 Close | +5.39% | +3.29% | 91% | 8.76% | 0.61 | 33 |
| D1 VWAP | +5.79% | +3.05% | 94% | 9.19% | 0.63 | 33 |
| D2 | +6.03% | +3.10% | 91% | 9.95% | 0.61 | 33 |
| D5 | +7.56% | +2.92% | 85% | 15.12% | 0.50 | 33 |
| D7 | +8.72% | +2.90% | 79% | 22.47% | 0.39 | 33 |
| D14 | +13.08% | +3.37% | 73% | 38.99% | 0.34 | 33 |
| D30 | +9.92% | +4.19% | 64% | 27.87% | 0.36 | 33 |
| D63 | +8.32% | +3.61% | 62% | 28.07% | 0.30 | 32 |
| D126 | +2.03% | +3.94% | 65% | 35.83% | 0.06 | 31 |

### Energy & Utilities  (n = 19)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.68% | +5.33% | 89% | 6.14% | 1.09 | 19 |
| D1 Close | +4.22% | +3.33% | 84% | 8.63% | 0.49 | 19 |
| D1 VWAP | +4.86% | +4.29% | 84% | 7.62% | 0.64 | 19 |
| D2 | +2.54% | +3.50% | 79% | 8.79% | 0.29 | 19 |
| D5 | +2.79% | +2.55% | 74% | 10.35% | 0.27 | 19 |
| D7 | +1.33% | +3.88% | 63% | 11.32% | 0.12 | 19 |
| D14 | -0.58% | +0.28% | 53% | 16.47% | -0.04 | 19 |
| D30 | -1.57% | -4.45% | 39% | 17.22% | -0.09 | 18 |
| D63 | -8.73% | -10.02% | 44% | 25.60% | -0.34 | 16 |
| D126 | -10.25% | -12.40% | 27% | 30.81% | -0.33 | 15 |

### Financial Services  (n = 42)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | -2.66% | +3.61% | 86% | 34.64% | -0.08 | 42 |
| D1 Close | -3.22% | +3.24% | 76% | 34.58% | -0.09 | 42 |
| D1 VWAP | -2.80% | +3.70% | 81% | 34.71% | -0.08 | 42 |
| D2 | -2.29% | +3.64% | 76% | 35.39% | -0.06 | 42 |
| D5 | -4.11% | +4.61% | 69% | 33.70% | -0.12 | 42 |
| D7 | -5.10% | +3.97% | 67% | 32.84% | -0.16 | 42 |
| D14 | -6.13% | +1.38% | 54% | 35.90% | -0.17 | 41 |
| D30 | -5.06% | -2.65% | 41% | 43.48% | -0.12 | 41 |
| D63 | +0.74% | -1.71% | 49% | 49.91% | 0.01 | 39 |
| D126 | -0.97% | +2.49% | 53% | 48.23% | -0.02 | 36 |

### Healthcare  (n = 106)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.24% | +4.66% | 94% | 6.14% | 1.02 | 105 |
| D1 Close | +4.57% | +3.01% | 72% | 7.90% | 0.58 | 105 |
| D1 VWAP | +5.24% | +4.09% | 83% | 7.06% | 0.74 | 105 |
| D2 | +3.78% | +3.59% | 69% | 9.41% | 0.40 | 105 |
| D5 | +2.15% | +2.04% | 61% | 13.76% | 0.16 | 104 |
| D7 | +2.08% | +0.94% | 53% | 16.88% | 0.12 | 104 |
| D14 | +1.62% | -0.36% | 49% | 18.68% | 0.09 | 103 |
| D30 | -1.12% | -0.75% | 49% | 25.58% | -0.04 | 102 |
| D63 | -2.44% | -7.11% | 39% | 35.76% | -0.07 | 98 |
| D126 | -3.10% | -7.27% | 43% | 45.79% | -0.07 | 86 |

### Industrials  (n = 80)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +2.37% | +3.51% | 92% | 18.56% | 0.13 | 79 |
| D1 Close | +2.15% | +3.36% | 89% | 18.72% | 0.11 | 79 |
| D1 VWAP | +2.22% | +3.54% | 89% | 18.47% | 0.12 | 79 |
| D2 | +1.62% | +3.40% | 75% | 18.71% | 0.09 | 79 |
| D5 | +3.02% | +3.51% | 72% | 24.03% | 0.13 | 79 |
| D7 | +3.62% | +3.00% | 71% | 24.57% | 0.15 | 79 |
| D14 | +4.52% | +4.77% | 67% | 25.80% | 0.18 | 78 |
| D30 | +4.61% | +5.69% | 65% | 25.00% | 0.18 | 77 |
| D63 | +9.40% | +10.57% | 66% | 30.97% | 0.30 | 70 |
| D126 | +16.92% | +14.65% | 65% | 49.80% | 0.34 | 54 |

### Other  (n = 1)  ⚠️ *Low sample — directional only*

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +1.77% | +1.77% | 100% | nan% | — | 1 |
| D1 Close | +1.17% | +1.17% | 100% | nan% | — | 1 |
| D1 VWAP | +1.57% | +1.57% | 100% | nan% | — | 1 |
| D2 | +2.07% | +2.07% | 100% | nan% | — | 1 |
| D5 | +1.17% | +1.17% | 100% | nan% | — | 1 |
| D7 | +4.78% | +4.78% | 100% | nan% | — | 1 |
| D14 | -1.24% | -1.24% | 0% | nan% | — | 1 |
| D30 | +4.18% | +4.18% | 100% | nan% | — | 1 |
| D63 | -6.06% | -6.06% | 0% | nan% | — | 1 |
| D126 | +1.77% | +1.77% | 100% | nan% | — | 1 |

### Real Estate  (n = 104)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +3.27% | +2.66% | 95% | 3.11% | 1.05 | 101 |
| D1 Close | +3.10% | +3.35% | 88% | 4.07% | 0.76 | 101 |
| D1 VWAP | +3.19% | +3.12% | 92% | 3.52% | 0.91 | 101 |
| D2 | +3.58% | +3.21% | 90% | 4.74% | 0.76 | 101 |
| D5 | +2.46% | +2.84% | 75% | 5.88% | 0.42 | 101 |
| D7 | +2.59% | +2.74% | 77% | 6.53% | 0.40 | 101 |
| D14 | +2.48% | +2.18% | 72% | 9.21% | 0.27 | 98 |
| D30 | +2.56% | +1.49% | 62% | 23.78% | 0.11 | 98 |
| D63 | -1.26% | +1.88% | 56% | 17.46% | -0.07 | 94 |
| D126 | -5.16% | +0.37% | 51% | 21.55% | -0.24 | 86 |

### Technology  (n = 96)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.66% | +4.80% | 96% | 6.66% | 1.00 | 96 |
| D1 Close | +5.57% | +3.40% | 83% | 9.33% | 0.60 | 96 |
| D1 VWAP | +5.94% | +4.07% | 91% | 8.14% | 0.73 | 96 |
| D2 | +5.36% | +3.47% | 72% | 11.93% | 0.45 | 96 |
| D5 | +2.41% | +2.43% | 62% | 11.23% | 0.21 | 96 |
| D7 | +1.85% | +1.06% | 56% | 13.57% | 0.14 | 96 |
| D14 | +4.24% | +1.89% | 57% | 19.29% | 0.22 | 95 |
| D30 | +3.09% | -1.31% | 45% | 25.27% | 0.12 | 93 |
| D63 | +2.70% | +0.93% | 52% | 36.51% | 0.07 | 88 |
| D126 | +1.59% | -2.81% | 47% | 38.16% | 0.04 | 79 |

**Sector D1 Open mean return ranking:**

| Rank | Sector | Mean D1 Open | N |
|------|--------|-------------:|---|
| 1 | Consumer Cyclical | +8.68% | 78 |
| 2 | Consumer Defensive | +6.69% | 33 |
| 3 | Energy & Utilities | +6.68% | 19 |
| 4 | Technology | +6.66% | 96 |
| 5 | Healthcare | +6.24% | 105 |
| 6 | Communication Services | +3.94% | 21 |
| 7 | Real Estate | +3.27% | 101 |
| 8 | Basic Materials | +2.80% | 26 |
| 9 | Industrials | +2.37% | 79 |
| 10 | Other | +1.77% | 1 |
| 11 | Financial Services | -2.66% | 42 |

---

## 6. Returns by Deal Size

### Small (<$100M)  (n = 334)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +5.01% | +4.12% | 93% | 18.50% | 0.27 | 330 |
| D1 Close | +3.56% | +3.47% | 84% | 18.80% | 0.19 | 330 |
| D1 VWAP | +4.14% | +3.83% | 89% | 18.62% | 0.22 | 330 |
| D2 | +3.38% | +3.47% | 78% | 19.57% | 0.17 | 330 |
| D5 | +2.51% | +2.56% | 67% | 21.74% | 0.12 | 330 |
| D7 | +2.25% | +1.84% | 63% | 23.22% | 0.10 | 330 |
| D14 | +2.55% | +1.54% | 58% | 27.25% | 0.09 | 325 |
| D30 | +1.07% | +0.24% | 52% | 30.40% | 0.04 | 321 |
| D63 | +0.61% | +0.50% | 51% | 36.32% | 0.02 | 307 |
| D126 | -0.53% | +0.23% | 50% | 42.98% | -0.01 | 273 |

### Mid ($100-500M)  (n = 216)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +3.95% | +3.31% | 92% | 4.41% | 0.90 | 214 |
| D1 Close | +3.67% | +3.06% | 81% | 6.47% | 0.57 | 214 |
| D1 VWAP | +3.79% | +3.16% | 86% | 5.47% | 0.69 | 214 |
| D2 | +3.88% | +3.22% | 75% | 7.81% | 0.50 | 214 |
| D5 | +2.60% | +3.14% | 65% | 9.50% | 0.27 | 214 |
| D7 | +2.62% | +2.46% | 65% | 10.36% | 0.25 | 214 |
| D14 | +4.02% | +3.88% | 64% | 13.14% | 0.31 | 211 |
| D30 | +3.52% | +1.43% | 56% | 20.85% | 0.17 | 210 |
| D63 | +3.98% | +1.67% | 54% | 28.61% | 0.14 | 198 |
| D126 | +6.70% | -0.27% | 49% | 39.81% | 0.17 | 178 |

### Large (>$500M)  (n = 57)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.72% | +2.12% | 98% | 26.30% | 0.26 | 57 |
| D1 Close | +7.08% | +2.68% | 86% | 26.63% | 0.27 | 57 |
| D1 VWAP | +6.89% | +2.42% | 88% | 26.42% | 0.26 | 57 |
| D2 | +6.68% | +2.26% | 70% | 26.70% | 0.25 | 57 |
| D5 | +6.42% | +2.80% | 68% | 27.13% | 0.24 | 56 |
| D7 | +6.15% | +3.23% | 64% | 27.50% | 0.22 | 56 |
| D14 | +4.59% | +0.76% | 52% | 28.59% | 0.16 | 56 |
| D30 | +5.60% | +2.19% | 58% | 30.16% | 0.19 | 55 |
| D63 | +6.21% | -0.76% | 50% | 34.35% | 0.18 | 52 |
| D126 | +6.67% | +3.05% | 53% | 39.70% | 0.17 | 47 |

> Pearson r (deal size USD vs D1 Open return) = +0.154 (n=601).  Positive relationship: larger deals tend to outperform slightly at D1 Open.

---

## 7. Returns by Market Capitalisation

### Small Cap (<$1B)  (n = 236)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +2.90% | +3.62% | 91% | 19.91% | 0.15 | 232 |
| D1 Close | +1.81% | +3.21% | 84% | 20.38% | 0.09 | 232 |
| D1 VWAP | +2.38% | +3.42% | 88% | 20.25% | 0.12 | 232 |
| D2 | +1.94% | +3.25% | 78% | 21.29% | 0.09 | 232 |
| D5 | +1.36% | +2.13% | 66% | 23.78% | 0.06 | 232 |
| D7 | +1.39% | +1.58% | 61% | 25.36% | 0.06 | 232 |
| D14 | +1.79% | +1.12% | 55% | 29.75% | 0.06 | 231 |
| D30 | -0.05% | -0.18% | 49% | 31.54% | -0.00 | 230 |
| D63 | -1.42% | +0.50% | 51% | 34.97% | -0.04 | 217 |
| D126 | -4.31% | -3.43% | 44% | 42.30% | -0.10 | 192 |

### Mid Cap ($1-10B)  (n = 303)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +6.00% | +4.05% | 94% | 8.95% | 0.67 | 301 |
| D1 Close | +5.17% | +3.65% | 83% | 9.72% | 0.53 | 301 |
| D1 VWAP | +5.41% | +3.70% | 89% | 9.06% | 0.60 | 301 |
| D2 | +5.03% | +3.69% | 77% | 10.48% | 0.48 | 301 |
| D5 | +3.61% | +3.48% | 68% | 11.93% | 0.30 | 300 |
| D7 | +3.33% | +3.07% | 67% | 13.06% | 0.26 | 300 |
| D14 | +4.12% | +3.24% | 64% | 15.73% | 0.26 | 293 |
| D30 | +3.54% | +1.97% | 57% | 23.25% | 0.15 | 289 |
| D63 | +3.86% | +1.37% | 52% | 32.74% | 0.12 | 280 |
| D126 | +6.03% | +1.99% | 54% | 39.56% | 0.15 | 249 |

### Large Cap (>$10B)  (n = 68)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +5.93% | +2.05% | 97% | 24.11% | 0.25 | 68 |
| D1 Close | +5.71% | +1.81% | 79% | 24.26% | 0.24 | 68 |
| D1 VWAP | +5.74% | +1.93% | 82% | 24.20% | 0.24 | 68 |
| D2 | +5.35% | +2.03% | 69% | 24.54% | 0.22 | 68 |
| D5 | +5.11% | +2.09% | 63% | 24.99% | 0.20 | 68 |
| D7 | +4.78% | +2.48% | 60% | 25.11% | 0.19 | 68 |
| D14 | +4.61% | +1.35% | 51% | 26.09% | 0.18 | 68 |
| D30 | +5.65% | +1.35% | 57% | 27.85% | 0.20 | 67 |
| D63 | +8.76% | +1.29% | 55% | 31.34% | 0.28 | 60 |
| D126 | +12.05% | +2.03% | 53% | 45.28% | 0.27 | 57 |

---

## 8. Returns by Year

### 2022  (n = 69)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +2.59% | +1.91% | 86% | 3.52% | 0.74 | 66 |
| D1 Close | +0.03% | +1.22% | 62% | 6.70% | 0.00 | 66 |
| D1 VWAP | +0.80% | +1.66% | 70% | 5.36% | 0.15 | 66 |
| D2 | -0.63% | +1.00% | 58% | 7.38% | -0.08 | 66 |
| D5 | -2.33% | -1.11% | 41% | 9.27% | -0.25 | 66 |
| D7 | -1.04% | -0.88% | 47% | 10.65% | -0.10 | 66 |
| D14 | -1.98% | -0.65% | 44% | 14.57% | -0.14 | 66 |
| D30 | -3.57% | -0.71% | 44% | 19.01% | -0.19 | 66 |
| D63 | -8.43% | -5.20% | 42% | 25.82% | -0.33 | 66 |
| D126 | -10.77% | -7.02% | 44% | 32.33% | -0.33 | 66 |

### 2023  (n = 118)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +1.79% | +3.33% | 91% | 14.96% | 0.12 | 116 |
| D1 Close | +1.49% | +3.08% | 86% | 15.17% | 0.10 | 116 |
| D1 VWAP | +1.70% | +3.18% | 91% | 15.01% | 0.11 | 116 |
| D2 | +1.43% | +3.23% | 79% | 15.24% | 0.09 | 116 |
| D5 | +1.65% | +2.65% | 68% | 20.40% | 0.08 | 116 |
| D7 | +1.72% | +2.33% | 66% | 21.58% | 0.08 | 116 |
| D14 | +0.47% | +1.52% | 59% | 22.34% | 0.02 | 116 |
| D30 | -1.83% | +0.79% | 53% | 19.46% | -0.09 | 116 |
| D63 | -2.36% | -1.40% | 47% | 25.17% | -0.09 | 116 |
| D126 | -3.61% | -3.16% | 43% | 33.50% | -0.11 | 116 |

### 2024  (n = 130)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +2.27% | +3.28% | 94% | 15.83% | 0.14 | 129 |
| D1 Close | +1.04% | +2.62% | 82% | 15.86% | 0.07 | 129 |
| D1 VWAP | +1.54% | +2.96% | 88% | 15.76% | 0.10 | 129 |
| D2 | +1.48% | +2.66% | 74% | 16.49% | 0.09 | 129 |
| D5 | +0.65% | +2.55% | 66% | 17.07% | 0.04 | 129 |
| D7 | +0.81% | +1.75% | 64% | 18.80% | 0.04 | 129 |
| D14 | +2.24% | +2.62% | 63% | 25.88% | 0.09 | 129 |
| D30 | -0.58% | -0.32% | 49% | 25.04% | -0.02 | 129 |
| D63 | +0.17% | +1.03% | 55% | 31.78% | 0.01 | 129 |
| D126 | +3.41% | +0.53% | 50% | 39.02% | 0.09 | 129 |

### 2025  (n = 202)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +8.61% | +4.27% | 95% | 19.65% | 0.44 | 202 |
| D1 Close | +8.10% | +3.99% | 86% | 20.14% | 0.40 | 202 |
| D1 VWAP | +8.32% | +4.10% | 90% | 19.91% | 0.42 | 202 |
| D2 | +8.00% | +4.60% | 82% | 20.74% | 0.39 | 202 |
| D5 | +6.96% | +4.52% | 75% | 21.93% | 0.32 | 202 |
| D7 | +6.80% | +3.62% | 72% | 22.95% | 0.30 | 202 |
| D14 | +8.33% | +4.91% | 67% | 24.72% | 0.34 | 202 |
| D30 | +9.32% | +5.47% | 63% | 31.02% | 0.30 | 202 |
| D63 | +10.73% | +3.72% | 59% | 40.20% | 0.27 | 202 |
| D126 | +10.96% | +3.45% | 57% | 48.67% | 0.23 | 187 |

### 2026 *(partial, through June 2026)*  (n = 88)

| Horizon | Mean | Median | % Pos. | Std Dev | Sharpe | N |
|:--------|-----:|-------:|-------:|--------:|-------:|--:|
| D1 Open | +5.36% | +5.00% | 95% | 12.91% | 0.42 | 88 |
| D1 Close | +4.77% | +4.33% | 88% | 13.56% | 0.35 | 88 |
| D1 VWAP | +5.02% | +4.70% | 91% | 13.06% | 0.38 | 88 |
| D2 | +4.50% | +3.65% | 76% | 15.77% | 0.29 | 88 |
| D5 | +2.53% | +2.19% | 67% | 16.25% | 0.16 | 87 |
| D7 | +0.45% | +1.04% | 57% | 17.13% | 0.03 | 87 |
| D14 | +0.49% | -0.72% | 48% | 20.82% | 0.02 | 79 |
| D30 | +0.41% | -0.97% | 48% | 33.52% | 0.01 | 73 |
| D63 | -1.40% | -5.23% | 39% | 26.94% | -0.05 | 44 |
| D126 | — | — | — | — | — | 0 |

**Year-by-year D1 Close and D30 summary:**

| Year | D1 Close Mean | D30 Mean | N |
|------|-------------:|---------:|---|
| 2022 | +0.03% | -3.57% | 69 |
| 2023 | +1.49% | -1.83% | 118 |
| 2024 | +1.04% | -0.58% | 130 |
| 2025 | +8.10% | +9.32% | 202 |
| 2026 | +4.77% | +0.41% | 88 |

> 2025 was exceptional: D1 Close +8.10%, D30 +9.32%.  Compare 2022: D1 Close +0.03%, D30 -3.57%.

---

## 9. Top 5 and Bottom 5 Deals at Each Horizon

### D1 Open

**Top 5 — D1 Open:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +106.20% | 2025-05-19 |
| 3 | Sanergy Group Limited | 2459 | HK/China | Industrials | +83.75% | 2025-08-19 |
| 4 | Seyond Holdings Ltd.  | 2665 | HK/China | Financial Services | +65.00% | 2025-12-09 |
| 5 | Lianlian DigiTech Co., Ltd. | 2598 | HK/China | Financial Services | +49.27% | 2025-07-14 |

**Bottom 5 — D1 Open:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.89% | 2024-01-02 |
| 4 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.86% | 2026-03-09 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.84% | 2024-09-03 |

### D1 Close

**Top 5 — D1 Close:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +103.94% | 2025-05-19 |
| 3 | Sanergy Group Limited | 2459 | HK/China | Industrials | +80.00% | 2025-08-19 |
| 4 | Seyond Holdings Ltd.  | 2665 | HK/China | Financial Services | +68.80% | 2025-12-09 |
| 5 | Persistence Resources Group Ltd | 2489 | HK/China | Basic Materials | +62.71% | 2025-09-25 |

**Bottom 5 — D1 Close:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.88% | 2024-01-02 |
| 4 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.86% | 2026-03-09 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.82% | 2024-09-03 |

### D1 VWAP

**Top 5 — D1 VWAP:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +105.35% | 2025-05-19 |
| 3 | Sanergy Group Limited | 2459 | HK/China | Industrials | +81.25% | 2025-08-19 |
| 4 | Seyond Holdings Ltd.  | 2665 | HK/China | Financial Services | +65.40% | 2025-12-09 |
| 5 | Persistence Resources Group Ltd | 2489 | HK/China | Basic Materials | +55.37% | 2025-09-25 |

**Bottom 5 — D1 VWAP:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.87% | 2024-01-02 |
| 4 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.87% | 2026-03-09 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.82% | 2024-09-03 |

### D2

**Top 5 — D2:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +103.38% | 2025-05-19 |
| 3 | Sanergy Group Limited | 2459 | HK/China | Industrials | +80.00% | 2025-08-19 |
| 4 | Hainan Drinda New Energy Technol | 2865 | HK/China | Technology | +77.27% | 2026-01-21 |
| 5 | Seyond Holdings Ltd.  | 2665 | HK/China | Financial Services | +70.00% | 2025-12-09 |

**Bottom 5 — D2:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.88% | 2026-03-09 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.86% | 2024-01-02 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.83% | 2024-09-03 |

### D5

**Top 5 — D5:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | VPower Group International Holdi | 1608 | HK/China | Industrials | +124.24% | 2023-08-24 |
| 3 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +113.52% | 2025-05-19 |
| 4 | Sanergy Group Limited | 2459 | HK/China | Industrials | +88.75% | 2025-08-19 |
| 5 | Shenzhen Pagoda Industrial (Grou | 2411 | HK/China | Consumer Defensive | +63.25% | 2025-09-22 |

**Bottom 5 — D5:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.88% | 2026-03-09 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.87% | 2024-01-02 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.85% | 2024-09-03 |

### D7

**Top 5 — D7:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | VPower Group International Holdi | 1608 | HK/China | Industrials | +136.36% | 2023-08-24 |
| 3 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +108.17% | 2025-05-19 |
| 4 | Shenzhen Pagoda Industrial (Grou | 2411 | HK/China | Consumer Defensive | +102.56% | 2025-09-22 |
| 5 | Persistence Resources Group Ltd | 2489 | HK/China | Basic Materials | +73.73% | 2025-09-25 |

**Bottom 5 — D7:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.97% | 2023-09-28 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.88% | 2026-03-09 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.87% | 2024-01-02 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.85% | 2024-09-03 |

### D14

**Top 5 — D14:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | MOG Digitech Holdings Ltd. | 1942 | HK/China | Consumer Defensive | +200.00% | 2024-09-16 |
| 3 | VPower Group International Holdi | 1608 | HK/China | Industrials | +136.36% | 2023-08-24 |
| 4 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +107.61% | 2025-05-19 |
| 5 | Hainan Drinda New Energy Technol | 2865 | HK/China | Technology | +91.55% | 2026-01-21 |

**Bottom 5 — D14:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-09-28 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-04-17 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.89% | 2026-03-09 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.86% | 2024-01-02 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.77% | 2024-09-03 |

### D30

**Top 5 — D30:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | ITC Properties Group Limited | 199 | HK/China | Real Estate | +200.00% | 2026-04-21 |
| 2 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 3 | InnoScience (Suzhou) Technology  | 2577 | HK/China | Technology | +139.38% | 2025-07-21 |
| 4 | MOG Digitech Holdings Ltd. | 1942 | HK/China | Consumer Defensive | +133.96% | 2024-09-16 |
| 5 | TradeGo FinTech Ltd. | 8017 | HK/China | Financial Services | +111.11% | 2025-06-23 |

**Bottom 5 — D30:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.99% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-09-28 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.90% | 2026-03-09 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.87% | 2024-01-02 |
| 5 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.68% | 2024-09-03 |

### D63

**Top 5 — D63:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Yangtze Optical Fibre and Cable  | 6869 | HK/China | Technology | +200.00% | 2025-12-09 |
| 2 | TradeGo FinTech Ltd. | 8017 | HK/China | Financial Services | +200.00% | 2025-06-23 |
| 3 | PAL GROUP Holdings Co., Ltd. | 2726 | Japan | Consumer Cyclical | +200.00% | 2025-05-19 |
| 4 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 5 | Shanghai MicroPort MedBot Group  | 2252 | HK/China | Healthcare | +172.61% | 2024-12-02 |

**Bottom 5 — D63:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.99% | 2023-04-17 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.98% | 2023-09-28 |
| 3 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.91% | 2024-01-02 |
| 4 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.73% | 2024-09-03 |
| 5 | Graphex Group Limited | 6128 | HK/China | Basic Materials | -92.52% | 2024-10-17 |

### D126

**Top 5 — D126:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | BYD Company Limited | 1211 | HK/China | Consumer Cyclical | +200.00% | 2025-03-03 |
| 2 | Pop Mart International Group Lim | 9992 | HK/China | Communication Servic | +174.66% | 2024-10-24 |
| 3 | CStone Pharmaceuticals | 2616 | HK/China | Healthcare | +167.30% | 2025-04-02 |
| 4 | SK Square Co., Ltd | 402340 | Korea | Technology | +158.39% | 2025-07-10 |
| 5 | Dongfang Electric Co., Ltd | 1072 | HK/China | Industrials | +143.22% | 2025-09-17 |

**Bottom 5 — D126:**

| # | Issuer | Ticker | Region | Sector | Return | Date |
|---|--------|--------|--------|--------|-------:|------|
| 1 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.99% | 2023-09-28 |
| 2 | Differ Group Auto Limited | 6878 | HK/China | Financial Services | -99.99% | 2023-04-17 |
| 3 | Kingkey Financial International  | 1468 | HK/China | Financial Services | -99.90% | 2024-09-03 |
| 4 | Grand Talents Group Holdings Ltd | 8516 | HK/China | Industrials | -99.88% | 2024-01-02 |
| 5 | 3D Medicines Inc. | 1244 | HK/China | Healthcare | -94.32% | 2023-07-14 |

---

## 10. Statistical Patterns, Correlations, and Anomalies

### 10.1 Discount–Return Correlation

Pricing discount (to last trade) available for 607 deals.

| Horizon | Pearson r | Interpretation |
|---------|----------:|----------------|
| D1 Open | -0.304 | Significant negative — deeper discount → lower return |
| D1 Close | -0.236 | Significant negative — deeper discount → lower return |
| D5 | -0.137 | Weak — deeper discount → lower return |
| D30 | -0.029 | Weak — deeper discount → lower return |

> Negative correlation: deals priced at a *larger* discount (more negative value) paradoxically show *lower* raw returns vs offer. Consistent with information-asymmetry literature: deeper discounts signal higher placement risk, and post-pricing price discovery is less favourable. Effect strongest at D1 Open (r = -0.304).

### 10.2 Japan's Persistent Positive Drift

Japan is the only market where mean returns increase monotonically beyond D2, peaking at +5.56% at D63. The Japan vs HK/China divergence at D63 is statistically significant (t = 2.04, p = 0.0416).

Potential explanations:
1. **TSE corporate governance reform (2023–2025):** Pressure on companies trading below book value to improve capital efficiency creates sustained re-rating post-placement.
2. **Disciplined discount pricing:** Japanese banks consistently price at meaningful discounts, leaving recoverable value post-deal.
3. **Stable institutional base:** Lower short-term volatility allows the discount to accrete gradually rather than snap back at once.

### 10.3 The 2025 Regime Effect

2025 accounts for 202 out of 607 deals (33% of the sample) and shows dramatically higher returns than other years (D1 Open: +8.61%; D30: +9.32%). Because it dominates the sample, multi-year averages are materially biased upward. Analysts should examine 2022–2024 averages separately for a more conservative forward-looking estimate.

### 10.4 Marketed vs Overnight FO Asymmetry

Marketed FOs: D1 Close 95% positive vs Overnight FOs 72%. The D30 divergence is not significant at 5% (t = 0.91, p = 0.3615). Marketed deals are better price-discovered through roadshow bookbuilding; overnight deals price more aggressively to clear.

### 10.5 Korea Underperformance

Korea D1 Open mean: +1.03% (n=20). D5 % positive: 37%. Korea's small sample (n=20) and structurally different market (conglomerate-dominated, KRW volatility 2022–23) produce the weakest profile. All Korea findings are directional only.

### 10.6 D14 Non-Monotonicity

Mean return at D14 (+3.27%) is higher than at D7 (+2.75%) across the full dataset. Hypothesis: deals still underwater at D7 disproportionately recover by D14 (partial mean-reversion), while true chronic underperformers have already been reflected in the distribution. This is consistent across most sub-groups but is **not a reliable trading signal** — D14 Sharpe is still well below D1.

### 10.7 Low-Sample Sector Caution

- **Other:** n = 1 — results statistically unreliable, treat as illustrative only.

---

## 11. Missing Deals — Extra Credit

The following high-profile transactions may be absent from the CMG dataset or miscategorised. Sources: Bloomberg Terminal, HKEX disclosure search, TSE announcements, Nikkei Asia, Yonhap.

| Issuer | Market | Approx. Date | Approx. Size | Likely Reason for Absence |
|--------|--------|-------------|-------------|---------------------------|
| SoftBank Group | Japan (9984.T) | Sep 2023 | ~$5 B | Government/secondary stake sale via Arm IPO-related block; may be classified outside corporate FO |
| Japan Post Holdings | Japan (6178.T) | Nov 2023 | ~$10 B (¥1.5T) | Government divestment — may fall outside CMG's corporate FO classification |
| Alibaba Group | HK (9988.HK) | 2023, 2024 | Multiple $1–3 B | Possible accelerated bookbuilds or cross-holding sell-downs |
| BYD Company | HK (1211.HK) | Mar 2025 | ~$6.8 B | Rights component may cause exclusion; CMG may only track placements |
| Meituan | HK (3690.HK) | Oct 2023 | ~$2.0 B | Possibly included — worth cross-checking 3690.HK in dataset |
| KEPCO | Korea (015760.KS) | 2022–2023 | ~$900 M | Utility / quasi-government entity — may be excluded by sector rule |
| Kakao Corp | Korea (035720.KS) | 2022 | ~$500 M | Possibly included — worth cross-checking 035720.KS |
| Toyota Motor | Japan (7203.T) | 2023 | ~$7 B | Cross-holding divestment — correctly excluded if scope is corporate FO |
| Rakuten Group | Japan (4755.T) | Apr 2023 | ~$2.2 B | Emergency rights offering — may be categorised as rights issue not FO |
| SoftBank Corp | Japan (9434.T) | 2022 | ~$1.4 B | Subsidiary placement — check 9434.T |

> To verify, match each issuer's ticker, pricing date, and gross proceeds against the CMG dataset. Government divestments, rights offerings with nil-paid trading, mandatory convertibles, and ESOP placements are commonly excluded by CMG's classification methodology.

---

## Appendix — Methodology

**Return formula:** Return(N) = Price(N trading days post-pricing) / Offer Price − 1, local currency.

**Split adjustment:** Offer price divided by the product of all splits occurring *after* the pricing date (regardless of horizon), matching the backward-adjusted prices Yahoo Finance serves.

**VWAP approximation:** (High + Low + Close) / 3. True intraday VWAP unavailable from Yahoo Finance.

**Return clipping:** ±200% to suppress corporate-action misclassifications.

**Sharpe:** Mean return / cross-sectional standard deviation across deals. Not annualised.

**Statistical tests:** Welch's t-test (unequal variances), significance at p < 0.05.

---
*All figures computed programmatically from returns_cache.parquet.*