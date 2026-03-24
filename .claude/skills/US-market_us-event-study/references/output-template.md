# Output Template: US Event Study

> Goal: summarize event-driven abnormal performance, persistence, and what would invalidate the conclusion.

## Event Study Report

### 1) Executive Summary (3–5 bullets)

- Event type: `[earnings / guidance / M&A / regulatory / litigation / macro / other]`.
- Immediate market reaction: `[strong positive / moderate positive / neutral / moderate negative / strong negative]`.
- The reaction appears `[understood / overextended / not fully priced / likely to mean revert]`.
- Confidence level is `[high / medium / low]` based on liquidity, overlap with broader market moves, and data quality.
- Key follow-up variables: `[list 2–4]`.

### 2) Event Definition

| Item | Value |
|---|---|
| Security / universe | — |
| Event name | — |
| Event date | — |
| Benchmark | S&P 500 / sector ETF / custom peer basket |
| Estimation window | — |
| Event windows | `[-1,+1]`, `[-3,+3]`, `[-5,+5]` |

### 3) Key Data Table

| Metric | Value | Interpretation |
|---|---:|---|
| `AR[0]` | — | — |
| `CAR[-1,+1]` | — | — |
| `CAR[-3,+3]` | — | — |
| `CAR[-5,+5]` | — | — |
| `CAR[+6,+20]` | — | — |
| Volume spike | — | — |
| Volatility change | — | — |

### 4) Interpretation

- Was the reaction idiosyncratic or market/sector-driven?
- Was the move mostly about fundamentals, guidance, or positioning?
- Has the event been followed by drift or reversal?
- What evidence would invalidate the current interpretation?

### 5) Risks and Monitoring

| Risk | Trigger | Monitor | Mitigation |
|---|---|---|---|
| Overlap with broader market move | Benchmark and peers moved similarly | Sector ETF, index return | Emphasize benchmark-adjusted results |
| One-day overreaction | Large day-0 move with weak follow-through | Post-event drift | Reduce confidence in persistence |
| Low liquidity distortion | Thin trading or after-hours gap complexity | Volume, spread, next-day follow-through | Lower confidence |
| Thesis reversal | Guidance or follow-up facts change | Revisions, management updates | Reassess event conclusion |

### 6) Next Steps

- Check follow-up disclosures, conference call remarks, or revised guidance.
- Monitor 20-day and 60-day post-event drift.
- Compare against prior analogous events if relevant.

### 7) Data Gaps / Confidence

- Missing data:
- Proxy used:
- Confidence level: High / Medium / Low

### 8) Disclaimer

> **Disclaimer**: This analysis is for informational and educational purposes only and does not constitute investment advice. Event-study outputs are sensitive to event dating, benchmark choice, and liquidity conditions.
