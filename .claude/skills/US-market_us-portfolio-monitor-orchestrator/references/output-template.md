# Output Template: US Portfolio Monitor Orchestrator

> Goal: consolidate exposures, concentration, liquidity, drawdown risk, and action items into a single portfolio monitoring report.

## US Portfolio Monitoring Report

### 1) Executive Summary (3–5 bullets)

- Overall portfolio condition is `[healthy / stretched / defensive / high risk]`.
- The biggest exposure concentration is in `[sector / factor / top holdings / macro driver]`.
- The main risk issue is `[concentration / drawdown risk / style drift / liquidity / correlation spike]`.
- Relative to the benchmark or mandate, the portfolio is `[aligned / moderately drifted / materially drifted]`.
- Next, monitor `[top-5 weight, factor exposure, liquidity, drawdown, stress-test sensitivity]`.

### 2) Portfolio Snapshot

| Metric | Value | Definition/Source | Notes |
|---|---:|---|---|
| Portfolio value | — | Latest holdings | — |
| Number of holdings | — | Holdings count | — |
| Top 5 weight | — | Concentration | Core risk |
| Sector concentration | — | Sector weights | Exposure map |
| Factor tilt | — | Growth/value/quality/etc. | Style risk |
| Volatility / max drawdown | — | Historical portfolio risk | Risk profile |
| Cash weight | — | Cash / equivalents | Buffer |
| Tracking error / active risk | — | Relative to benchmark | If applicable |

### 3) Interpretation

#### 3.1 Exposure profile

- Where the portfolio is most exposed by sector, style, or macro sensitivity.
- Whether active tilts are intentional or due to drift.
- Which exposures matter most in the current regime.

#### 3.2 Risk condition

- Whether diversification is working or correlations are rising.
- How much low-liquidity or event-risk exposure exists.
- Which holdings contribute the most to risk and drawdown.

#### 3.3 Recommended actions

- Which holdings or exposures need immediate attention.
- Whether rebalancing, hedging, or deeper research is most appropriate.
- What threshold would trigger a formal portfolio adjustment.

### 4) Risks and Monitoring

| Risk | Trigger | Monitor | Mitigation / what changes the view |
|---|---|---|---|
| Concentration risk | Top names keep growing as winners | Top-5 weight, HHI | Trim and rebalance |
| Style drift | Growth/value tilt moves too far | Factor exposures | Reset toward target |
| Liquidity mismatch | Lower-liquidity positions grow | ADV %, spread | Reduce trade size / exposure |
| Stress sensitivity | Portfolio underperforms in stress tests | Scenario losses, beta | Add hedges or lower risk |

### 5) Next Steps

- Build a recurring dashboard cadence: daily / weekly / monthly.
- Link the most important positions to earnings, liquidity, and valuation monitors.
- Define explicit thresholds for rebalancing and risk escalation.

### 6) Data Gaps / Confidence

- Missing data: real-time holdings drift, intraday risk exposures, derivative overlays.
- Proxy used: current holdings, historical returns, liquidity metrics, and stress-test assumptions.
- Confidence level: Medium.

### 7) Disclaimer

> **Disclaimer**: This analysis is for informational and educational purposes only and does not constitute investment advice. Portfolio monitoring is only as accurate as the holdings and assumptions supplied to it.
