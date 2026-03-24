# Output Template: US Liquidity Impact Estimator

> Goal: estimate whether a stock or portfolio can be traded efficiently, at what size, and with what likely market impact.

## US Liquidity and Impact Report

### 1) Executive Summary (3–5 bullets)

- The current liquidity condition is `[excellent / good / moderate / weak]`.
- The planned order size of `—` represents `—%` of `[ADV20 / ADV60]`, implying `[low / moderate / high]` impact risk.
- Estimated execution cost is `—` bps under `[normal / stressed]` conditions.
- The main cost driver is `[spread / volatility / thin depth / event-day conditions / concentrated order size]`.
- Next, monitor `[ADV, spread, intraday volatility, event calendar, participation rate]`.

### 2) Key Data Table

| Metric | Value | Definition/Source | Notes |
|---|---:|---|---|
| ADV20 / ADV60 | — | Average daily dollar volume | Base liquidity anchor |
| Bid-ask spread | — | Spread or proxy | Explicit cost |
| Realized volatility | — | Historical volatility | Impact amplifier |
| Planned order size | — | User-defined | Execution input |
| Participation rate | — | Order size / ADV | Execution burden |
| Estimated shortfall | — | Cost estimate | Model output |
| Days to liquidate | — | Size / expected daily participation | Practical view |

### 3) Interpretation

#### 3.1 Can this be traded efficiently

- Explain whether the order can be done in one day or should be staged.
- Identify whether the main issue is spread, depth, or event volatility.
- State how current liquidity compares with normal conditions.

#### 3.2 Cost and impact logic

- Link participation rate to expected slippage.
- Explain how volatility and spread change the cost curve.
- Distinguish normal-day assumptions from stressed-day assumptions.

#### 3.3 Execution recommendations

- Suggest immediate, staged, or algorithmic execution.
- State maximum sensible participation rate.
- Identify when the order should be delayed or reduced.

### 4) Risks and Monitoring

| Risk | Trigger | Monitor | Mitigation / what changes the view |
|---|---|---|---|
| Impact is underestimated | ADV drops or vol spikes | ADV, vol, spread | Reduce size or extend horizon |
| Event risk distorts execution | Earnings or news day | Event calendar, gap risk | Avoid normal-day assumptions |
| Liquidity vanishes in stress | Spread widens sharply | Spread, intraday range | Pause or stagger trades |
| Portfolio liquidation is harder than expected | Low-liquidity names dominate | Name-level ADV %, concentration | Sequence exits by liquidity |

### 5) Next Steps

- Re-run the estimate under normal and stressed conditions.
- Set a max participation-rate rule before execution.
- For portfolios, create a name-by-name liquidation ladder.

### 6) Data Gaps / Confidence

- Missing data: full order-book depth, dark-pool access, execution algorithm detail.
- Proxy used: ADV, spread, volatility, and participation-based impact assumptions.
- Confidence level: Medium.

### 7) Disclaimer

> **Disclaimer**: This analysis is for informational and educational purposes only and does not constitute investment advice. Liquidity impact is path-dependent and can change rapidly around events, volatility shocks, and market-stress episodes.
