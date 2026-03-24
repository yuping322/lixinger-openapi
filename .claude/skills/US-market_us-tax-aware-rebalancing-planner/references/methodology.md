# Methodology: US Tax-Aware Rebalancing Planner

This document defines the decision framework for rebalancing a taxable US portfolio while minimizing avoidable tax drag. The goal is not to avoid taxes at all costs, but to maximize after-tax portfolio improvement per unit of realized tax cost.

## Data Definitions

### Required inputs

For each holding or tax lot, collect:

- Ticker / asset name
- Quantity and current market value
- Cost basis per lot
- Unrealized gain or loss per lot
- Acquisition date and holding period
- Account type (taxable / IRA / Roth / 401k / etc.)
- Target weight or target range
- Liquidity and spread considerations

Portfolio-level inputs:

- Cash contribution / withdrawal needs
- Risk limits and drift tolerance
- Assumed federal and state tax rates if known
- Wash-sale constraints across accounts if relevant

### Frequency and windows

- Current weights: latest prices
- Tax status: lot-level as of analysis date
- Drift review: monthly by default, sooner if weight drift is large
- Tax-loss harvesting review: year-round, with more attention near year-end

## Core Metrics

### Position drift and trading need

- `Weight drift = current weight - target weight`
- `Absolute drift = |current weight - target weight|`
- `Relative drift = current weight / target weight - 1`

Suggested initial attention thresholds:

- `Absolute drift >= 3pp`, or
- `Relative drift >= 20%`

### Tax cost estimation

- `Realized gain = sale proceeds - cost basis`
- `Estimated tax cost = realized gain × applicable tax rate`
- `After-tax proceeds = sale proceeds - estimated tax cost`

Distinguish clearly between:

- Short-term gains
- Long-term gains
- Harvestable losses
- Tax-neutral trades in sheltered accounts

### After-tax efficiency

Use a simple priority framing:

- `Rebalance benefit` = risk reduction + target alignment + cash need fulfillment
- `Tax friction` = estimated tax cost + wash-sale constraint + liquidity cost
- `Priority` is high when benefit is large and tax friction is low

### Loss harvesting value

- `Harvest value = realized loss × marginal tax rate`
- Replace harvested positions with a sufficiently differentiated substitute to reduce wash-sale risk

## Signals and Thresholds

### High-priority rebalance actions

Typically prioritize when at least one of the following is true:

- Position exceeds target by `>= 5pp`
- A single name breaches concentration limits
- Portfolio factor risk materially exceeds budget
- Required cash needs cannot be met without action
- Harvestable losses are meaningful and substitutes exist

### Low-priority / defer candidates

Prefer to defer when:

- Drift is small (`< 2pp`) and tax cost is high
- Gains are short-term and can become long-term soon
- The trade improves alignment only marginally
- Liquidity is poor or spreads are punitive

### Trigger / exit / invalidation

- **Trigger** review when drift breaches tolerance bands, cash needs change, or tax-loss opportunities open up
- **Exit** once the portfolio returns to target range and tax budget is respected
- **Invalidate** the plan if lot data is incomplete, tax status is uncertain, or cross-account wash-sale exposure is not understood

### Threshold rationale

- `2pp ~ 3pp` drift is usually enough to matter for diversified portfolios without forcing noise trading
- `5pp` or more often indicates a true rebalance need rather than routine market movement
- Separate thresholds for short-term vs long-term gains prevent expensive over-trading

## Edge Cases and Degradation

### Missing or incomplete tax-lot data

- If lot-level basis is unavailable, produce a provisional plan only
- Mark all tax estimates as approximate
- Focus on account-level or sleeve-level actions until lot data is restored

### Wash-sale awareness

- Avoid recommending a sale-loss-harvest plus near-identical repurchase inside 30 days
- Review linked accounts when possible
- If replacement security similarity is uncertain, downgrade confidence

### Asset-specific considerations

- ETFs often have efficient substitute options; single stocks usually do not
- Mutual funds may have capital gain distributions that complicate timing
- Restricted stock, options, and employer stock may require separate handling

## Interpretation Rules

A good tax-aware rebalance plan should explicitly answer:

1. Which trades are necessary now?
2. Which trades should be delayed to reduce tax drag?
3. Where can contributions or withdrawals do the work instead of selling?
4. What is the estimated tax budget, and what assumptions drive it?
