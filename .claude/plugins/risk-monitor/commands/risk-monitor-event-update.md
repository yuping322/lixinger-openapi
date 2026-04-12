---
description: 持仓后事件驱动增量更新，识别新增事件并触发规则重算
argument-hint: "[watchlist] [--event-window 24h|3d] [--event-sources announcement|news|market_anomaly]"
target-skill: "risk-monitor-orchestrator"
output-format: "event-driven-risk-update-output-template"
risk-level: "medium"
---

# /risk-monitor-event-update

持仓后事件驱动增量更新（公告/新闻/异动触发），识别新增事件并定位触发规则。

## 路由行为

加载 `risk-monitor-orchestrator` skill 后执行：
1. 解析 watchlist、event_window、event_sources 参数
2. 过滤相关规则（event_triggers.source 匹配）
3. 对受影响股票执行规则重算
4. 输出新增/升级/解除告警

## 参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `watchlist` | array/string | 是 | 股票代码列表 |
| `event_window` | string | 否 | `24h` / `3d`，默认 `24h` |
| `event_sources` | array | 否 | `announcement` / `news` / `market_anomaly`，默认全部 |

> 注：`filing_update` 和 `manual` 由规则引擎内部触发，不在命令层暴露。

## 事件路由

| event_source | 触发规则类型 |
|--------------|-------------|
| announcement | pledge_update, unlock_notice, financial_report, major_event |
| news | negative_news, regulatory_action, industry_warning |
| market_anomaly | volume_spike, price_gap, limit_up_down_chain |

## 输出契约

必须包含：
- 新增告警（alert_id, risk_type, severity, thesis）
- 升级告警（原等级 → 新等级）
- 解除告警（invalidation_conditions 满足）
- 下次复核时间

## 示例

```bash
/risk-monitor-event-update '["600519"]' --event-window 24h --event-sources announcement,news
/risk-monitor-event-update my_watchlist --event-window 3d --event-sources market_anomaly
```