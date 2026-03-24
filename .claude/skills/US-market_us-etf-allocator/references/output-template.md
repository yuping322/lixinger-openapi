# Output Template: US ETF Allocator

> Goal: create a practical ETF allocation plan with exposure logic, liquidity checks, tracking considerations, and rebalancing rules.

## US ETF Allocation Report

### 1) Executive Summary (3–5 bullets)

- The recommended portfolio objective is `[core beta / tactical rotation / defensive mix / thematic allocation / income]`.
- The proposed ETF mix is `[list 3–6 ETFs]`, designed to express `[sector / factor / style / duration / income]` views.
- The portfolio’s main exposure tilt is toward `[large cap / growth / value / dividend / international / fixed income]`.
- The main trade-off is `[higher expected return vs higher tracking error / lower fee vs narrower exposure / better liquidity vs less precision]`.
- Next, monitor `[exposure drift, liquidity, tracking difference, cost, factor rotation]`.

### 2) Allocation Table

| ETF | Exposure | Target weight | Role | ADV / liquidity | Expense ratio / tracking notes |
|---|---|---:|---|---:|---|
| — | — | — | Core / Satellite | — | — |
| — | — | — | Core / Satellite | — | — |
| — | — | — | Core / Satellite | — | — |

### 3) Interpretation

#### 3.1 Exposure design

- Explain why each ETF is in the mix.
- Clarify sector, style, factor, and macro sensitivity.
- State whether the goal is benchmark-like exposure or active tilts.

#### 3.2 Implementation quality

- Assess liquidity, spread, and market depth.
- Explain any overlap between ETFs and whether it is intentional.
- Highlight tracking difference or methodology differences that matter.

#### 3.3 Portfolio trade-offs

- What the allocator is gaining by choosing these ETFs.
- What risks or compromises remain.
- Under what conditions the current mix should be reconsidered.

### 4) Risks and Monitoring

| Risk | Trigger | Monitor | Mitigation / what changes the view |
|---|---|---|---|
| Exposure overlap is too high | Multiple ETFs own the same names | Holdings overlap, concentration | Simplify the ETF mix |
| Tracking difference widens | ETF diverges from expected benchmark | Tracking difference, methodology | Replace or downgrade weight |
| Liquidity deteriorates | Spread or ADV worsens | Bid-ask, ADV | Limit trade size |
| Factor regime shifts | Style or sector leadership reverses | Relative returns, breadth | Rebalance tilt exposures |

### 5) Next Steps

- Validate overlap and effective exposure after aggregation.
- Set a calendar or threshold rebalancing rule.
- Compare the proposed mix against low-cost alternatives.

### 6) Data Gaps / Confidence

- Missing data: full real-time holdings, basket-level tax considerations, execution venue detail.
- Proxy used: ETF holdings summaries, liquidity metrics, fees, and exposure classifications.
- Confidence level: Medium.

### 7) Disclaimer

> **Disclaimer**: This analysis is for informational and educational purposes only and does not constitute investment advice. ETF allocation outcomes depend on product design, trading costs, tracking quality, and market regime changes.
