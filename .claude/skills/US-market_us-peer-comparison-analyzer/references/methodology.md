# Methodology: US Peer Comparison Analyzer

This document defines the comparison framework for peer-relative analysis. The objective is to explain why a company trades at a premium or discount to peers by decomposing differences in growth, profitability, balance-sheet quality, capital intensity, and valuation.

## Data Definitions

### Sources and field mapping

Preferred inputs:

1. **Market data**
   - Price, market cap, enterprise value, 52-week range, beta
2. **Financial statements**
   - Revenue, gross profit, EBIT, EBITDA, net income, free cash flow
   - Total assets, net debt, invested capital
3. **Estimates / forward data** (if available)
   - Next fiscal year revenue growth, EPS growth, forward EBITDA
4. **Company metadata**
   - Sector, sub-industry, geography, business model, fiscal year-end

### Frequency and windows

- Price / valuation: latest close and trailing 1-year range
- Income and cash flow: TTM plus last 3 fiscal years
- Balance-sheet items: latest quarter and prior fiscal year
- Default comparison horizon: current, 1-year history, 3-year operating trend

## Core Metrics

### Metric groups and formulas

#### 1. Scale and growth

- `Revenue growth = (Revenue_t / Revenue_{t-1}) - 1`
- `EPS growth = (EPS_t / EPS_{t-1}) - 1`
- `3-year CAGR = (Ending / Beginning)^(1/3) - 1`

#### 2. Profitability and efficiency

- `Gross margin = Gross profit / Revenue`
- `EBIT margin = EBIT / Revenue`
- `FCF margin = Free cash flow / Revenue`
- `ROIC = NOPAT / Invested capital`

#### 3. Balance-sheet quality

- `Net debt / EBITDA`
- `Interest coverage = EBIT / Interest expense`
- `Cash conversion = Free cash flow / Net income`

#### 4. Valuation

Use the most relevant set based on business model:

- `P/E`, `EV/EBITDA`, `EV/Sales`, `P/FCF`
- For capital-light growers: `EV/Sales`, Rule of 40, FCF inflection
- For mature cash generators: `P/E`, `P/FCF`, dividend yield

#### 5. Relative positioning

- `Premium / discount = Company multiple / Peer median - 1`
- `Percentile rank = rank(metric within peer set)`
- `Composite peer score = weighted average of growth, profitability, leverage, valuation`

### Standardization

- Use **peer median** as the default comparison anchor
- Use **percentile ranks** for simple relative positioning
- Use **z-scores** only when the peer set is large enough and not dominated by outliers
- Winsorize obvious outliers before scoring when needed

## Signals and Thresholds

### Premium / discount interpretation

#### Deserved premium

Typically supported when at least 3 conditions hold:

- Revenue growth is above peer median by `>= 5pp`
- EBIT margin or FCF margin is above peer median by `>= 3pp`
- Net debt / EBITDA is below peer median
- ROIC is above peer median

#### Potential value trap

A cheap stock should be flagged when:

- Valuation is below peer median by `>= 20%`
- Growth and margins are both below peer median
- Balance-sheet risk is worse than peer median

#### Quality at a reasonable price

Useful when:

- Profitability and balance-sheet quality rank in top third
- Valuation is near peer median or only modestly above it (`< 15% premium`)
- Cash conversion is stable

### Trigger / exit / invalidation

- **Trigger deeper review** when premium/discount moves `>= 15%` without a matching change in fundamentals
- **Exit a strong view** when the valuation gap closes and fundamentals no longer diverge
- **Invalidate the comparison** if peer composition changes materially, business models differ too much, or one-off items dominate reported results

### Threshold rationale

- `5pp` growth gaps and `3pp` margin gaps are large enough to matter economically in most sectors
- `15% ~ 20%` valuation gaps are typically meaningful after routine market noise
- Top-third / bottom-third cutoffs work well for small-to-medium peer sets

## Edge Cases and Degradation

### Missing data / outliers

- Negative earnings: de-emphasize P/E and shift to EV/Sales, EV/EBITDA, P/FCF
- Pre-revenue biotech or early-stage software: use business-model-specific metrics instead of forcing generic multiples
- Financials, insurers, REITs: use sector-appropriate metrics and do not mix with industrial frameworks
- Large one-off gains/losses: rely on adjusted or normalized earnings where available

### Fallback proxies

- No forward estimates: use trailing growth plus management guidance
- No clean ROIC: use ROE / asset turns / incremental margin as substitutes
- Limited peer history: compare against sector median and note lower confidence

## Interpretation Rules

A good peer-comparison output should answer four questions explicitly:

1. Why does the company deserve a premium or discount?
2. Which metric gap matters most: growth, margin, balance sheet, or cash flow?
3. What would cause the relative multiple to re-rate?
4. What evidence would invalidate the current thesis?
