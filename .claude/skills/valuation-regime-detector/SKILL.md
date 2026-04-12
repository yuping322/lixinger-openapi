---
name: valuation-regime-detector
description: Detect valuation regimes using historical/peer percentiles and macro/rate signals for China/US/HK markets. Use when asking whether a market/sector/stock is expensive/cheap or needs valuation percentile analysis.
parameters:
  market:
    type: string
    enum: [china, us, hk]
    default: china
    description: Target market for valuation analysis
---

# Valuation Regime Detector (Multi-Market)

Act as a professional research and risk analyst. Use a structured workflow to produce reusable analysis and monitoring checklist for valuation regimes across different markets.

## Workflow

### Step 1: Confirm Inputs

Confirm with the user:
- **Target universe**: market/sector/stock codes
- **Market parameter**: china/us/hk (defaults to china if not specified)
- **Time window**: historical lookback period
- **Output preference**: ranked list / brief / memo
- **Constraints**: liquidity, risk budget, mandate

### Step 2: Pull Data (Market-Specific)

Based on `market` parameter, use appropriate data sources:

**China Market**:
- Data fetching: see `references/data-queries-china.md`
- Key APIs: `cn/company/fundamental/non_financial`, `cn/index/fundamental`
- If specific data unavailable: state the gap and request alternative inputs

**US Market**:
- Data fetching: see `references/data-queries-us.md`
- Key APIs: `us/company/fundamental/non_financial`, `us/index/candlestick`, macro data
- If specific data unavailable: state the gap and request alternative inputs

**HK Market**:
- Data fetching: see `references/data-queries-hk.md` (if available)
- Otherwise: proxy using China market APIs with HK-listed stock codes
- Mark data quality limitations

### Step 3: Analysis Framework (Market-Adapted)

Use market-specific methodology:

**For China Market**: follow `references/methodology-china.md`
- Core metrics: PE, PB, dividend yield, ERP (vs 10Y treasury)
- Key rules: valuation repair, compression, turning points, equity-bond comparison
- Special considerations: A-share characteristics (T+1, limit up/down, suspended trading)
- Confidence factors: A-share market-specific signals

**For US Market**: follow `references/methodology-us.md`
- Core metrics: CAPE, Forward P/E, Earnings Yield, EV/EBITDA
- Key rules: cheap regime → long-horizon returns, expensive + rising rates → lower returns
- Conditioning variables: real rates, credit stress (HY OAS)
- Confidence factors: US market-specific signals

**For HK Market**: use China methodology with HK-specific adaptations
- Adjust for HK market structure (no limit up/down, different trading rules)
- Use HK-specific indices (HSI, HSCEI)
- Consider southbound capital flows impact on valuation

- Lead with executive summary (3–5 bullets), then show evidence
- Definitions, thresholds, edge cases in methodology files

### Step 4: Output

Generate final deliverable using market-appropriate template:

**China/HK**: Use `references/output-template-china.md` (Chinese output)
**US**: Use `references/output-template-us.md` (English output)

Include: key data, interpretation, risks, monitoring checklist, next steps.

## Market-Specific Considerations

### China Market Characteristics
- **T+1 trading**: cannot buy and sell same day
- **Limit up/down**: 10% daily limit for most stocks, 20% for ChiNext/STAR Market
- **Suspended trading**: can impact valuation interpretation and tradability
- **Regulatory announcements**: may lag and significantly impact conclusions
- **Valuation central tendency**: A-share valuation central tendency has long-term downward drift

### US Market Characteristics
- **No daily limits**: valuations can adjust rapidly
- **Real rates sensitivity**: direct link to bond market
- **Credit stress**: high yield spreads as leading indicator
- **Market breadth**: important conditioning variable

### HK Market Characteristics
- **No daily limits**: similar to US
- **Southbound flows**: mainland capital impact on valuation
- **Dual-listing impact**: A+H premium/discount analysis
- **Currency impact**: HKD/USD peg affects international comparisons

## Input Schema

```json
{
  "market": "china|us|hk",
  "target": "market|sector|stock",
  "codes": ["optional stock/sector codes"],
  "time_window": "1y|3y|5y|10y",
  "output_format": "list|brief|memo",
  "constraints": {
    "liquidity": "optional",
    "risk_budget": "optional"
  }
}
```

## Output Schema

```json
{
  "regime": "cheap|fair|rich|extreme",
  "valuation_percentile": "number",
  "key_metrics": {
    "pe": "number",
    "pb": "number",
    "ev_ebitda": "number (optional)",
    "dividend_yield": "number (optional)"
  },
  "drivers": ["list of key drivers"],
  "risks": ["list of identified risks"],
  "monitoring_points": ["list of items to monitor"],
  "confidence": "number (0-1)",
  "confidence_factors": ["list of factors affecting confidence"],
  "next_steps": ["list of recommended actions"],
  "data_gaps": ["list of missing data and proxies used"]
}
```

## Failure Modes (Market-Specific)

### China Market Failures
- Earnings data missing: use forecasts, mark as "using forecasts"
- Historical data insufficient (<5y): shorten lookback, mark as "insufficient history"
- PE < 0 (loss): use PB instead, mark as "using PB"
- Regulatory changes: invalidate historical regime comparisons

### US Market Failures
- Earnings collapse distorts P/E: use normalized earnings or price-to-sales
- Real rate regime shift: re-establish valuation regime from new regime
- Credit stress spike: reduce confidence in forward return expectations
- Structural market changes: historical relationships may no longer apply

### HK Market Failures
- Southbound flow disruption: reduce confidence in A+H premium signals
- Dual-listing suspended: limit comparable universe
- Currency peg stress: adjust international comparisons

## Confidence Sources

Confidence scores derive from:
1. **Data quality**: completeness and timeliness of valuation data
2. **Historical depth**: longer lookback periods increase confidence
3. **Cross-validation**: multiple valuation metrics agreement
4. **Conditioning variables**: macro/rate/credit signals alignment
5. **Market structure stability**: absence of regime-changing events

## Minimal Examples

### Example 1: China Market - Low Valuation Repair

**Input**: `{market: "china", target: "market", codes: ["000001"], time_window: "10y"}`
**Data**:
- PE percentile: 25%
- Earnings growth: +12%
- PEG: 0.8
**Output**:
- Regime: cheap
- Signal: Low valuation + earnings improvement → valuation repair
- Confidence: 0.68
- Conclusion: Valuation at bottom, earnings improving, 6-12 month repair expected

### Example 2: US Market - Expensive Regime

**Input**: `{market: "us", target: "market", codes: ["SPY"], time_window: "10y"}`
**Data**:
- Valuation percentile: 75%
- Earnings growth: +3%
- Real rates: rising +50bps
**Output**:
- Regime: rich
- Signal: Expensive + rising real rates → lower forward returns
- Confidence: 0.64
- Conclusion: Valuation elevated, real rates rising, 1-3 year return risk

### Example 3: HK Market - Southbound Flow Impact

**Input**: `{market: "hk", target: "market", codes: ["HSI"], time_window: "5y"}`
**Data**:
- PE percentile: 35%
- Southbound net inflow: positive
- A+H premium: narrowing
**Output**:
- Regime: below-average
- Signal: Southbound flows supporting valuation
- Confidence: 0.55 (lower due to HK-specific factors)
- Conclusion: Mainland capital flows providing valuation support

## Important Guidelines

- Always state data as-of dates and units; never fabricate missing values
- Separate signal from story: show what would change your conclusion
- Market-specific characteristics must be explicitly addressed
- This output is informational only and not investment advice

## Data Enhancement

For live market data, see market-specific data-queries files and use the shared lixinger query tool.