# Output Template: US Options Strategy Analyzer

> Goal: match the options structure to the investor’s view, risk tolerance, and event setup, rather than discussing strategies in isolation.

## Options Strategy Analysis Report

### 1) Executive Summary (3–5 bullets)

- The preferred strategy is `[covered call / cash-secured put / bull call spread / put spread / collar / iron condor / other]`.
- The strategy fits a view of `[bullish / mildly bullish / neutral / bearish / volatility-selling / event hedge]`.
- The main attraction is `[income / defined risk / leverage / downside buffer / volatility expression]`.
- The biggest risk is `[assignment / gap risk / volatility crush / limited upside / theta bleed]`.
- Next, monitor `[implied volatility, delta, theta, underlying move, event calendar]`.

### 2) Strategy Setup Table

| Item | Value |
|---|---|
| Underlying | — |
| Strategy type | — |
| Expiration | — |
| Strike(s) | — |
| Net premium | — |
| Max gain | — |
| Max loss | — |
| Break-even | — |

### 3) Greeks / Structure Snapshot

| Metric | Value | Meaning |
|---|---:|---|
| Delta | — | Directional sensitivity |
| Gamma | — | Convexity / acceleration |
| Theta | — | Time decay |
| Vega | — | Vol sensitivity |
| IV percentile | — | Relative richness of vol |
| Reward-to-risk | — | Structural attractiveness |

### 4) Interpretation

#### 4.1 Why this structure fits

- Connect the strategy directly to the underlying thesis.
- Explain why options are preferable to stock or a simpler structure.
- Clarify the time horizon and event dependence.

#### 4.2 Payoff logic

- What happens if the stock rallies, trades sideways, or sells off.
- How IV expansion or crush changes the outcome.
- Where the structure starts to fail relative to the original view.

#### 4.3 Execution and management

- When to take profits, cut losses, or roll the position.
- Whether assignment risk or early exercise matters.
- How liquidity and bid-ask spreads affect real execution quality.

### 5) Risks and Monitoring

| Risk | Trigger | Monitor | Mitigation / what changes the view |
|---|---|---|---|
| Volatility crush | Event passes and IV collapses | IV rank, event calendar | Prefer defined-risk spreads |
| Wrong directional timing | Underlying moves slowly or opposite | Delta, price path | Reassess horizon or structure |
| Liquidity is poor | Wide bid-ask spreads | Option volume, open interest | Avoid complex structures |
| Payoff cap is too restrictive | Covered calls cap upside | Underlying momentum | Roll or use wider strikes |

### 6) Next Steps

- Confirm open interest and bid-ask quality on the selected strikes.
- Run scenario analysis for price move and IV change.
- Define entry, take-profit, stop, and roll rules before execution.

### 7) Data Gaps / Confidence

- Missing data: real-time options chain depth, skew, market maker behavior.
- Proxy used: strategy payoff metrics, Greeks, implied volatility, and underlying thesis.
- Confidence level: Medium.

### 8) Disclaimer

> **Disclaimer**: This analysis is for informational and educational purposes only and does not constitute investment advice. Options involve leverage, time decay, and liquidity risks that can produce losses larger or faster than expected.
