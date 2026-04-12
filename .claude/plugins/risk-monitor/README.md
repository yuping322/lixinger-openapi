# Risk Monitor Plugin

面向“选股后排雷 + 持仓后事件跟踪”的风险插件。

## 当前阶段目标

1. **旧能力迁移（不整合）**：将 9 个既有风险 skill 原样迁移到 `skills/legacy/`。
2. **新引擎重开发**：在 `skills/risk-signal-engine/` 内建立独立规则引擎规范与可扩展规则目录。
3. **事件相关覆盖**：支持公告/新闻/异动触发的持仓后增量重算。

## 目录

- `skills/legacy/`：旧 skill 原样迁移区（仅迁移，不改造）
- `skills/risk-signal-engine/`：新规则引擎（重开发）
- `skills/risk-monitor-orchestrator/`：编排层（后续接入）
- `templates/`：能力矩阵、规则 schema、排雷输出模板
- `commands/`：命令入口

## 迁移清单（9个）

- equity-pledge-risk-monitor
- shareholder-risk-check
- shareholder-structure-monitor
- goodwill-risk-monitor
- st-delist-risk-scanner
- ipo-lockup-risk-monitor
- margin-risk-monitor
- limit-up-limit-down-risk-checker
- liquidity-impact-estimator

## 开发策略

- 在迁移完成前，不对 `skills/legacy/*` 做逻辑改造。
- 新逻辑仅放在 `risk-signal-engine`，通过规则文件迭代。
- 输出必须是"问题发现导向"，而非仅指标转述。
- 路径规范详见 `templates/path-conventions.md`。
- 事件源定义详见 `templates/event-source-dictionary.json`。

## Event Source Dictionary

### 规范事件源枚举

| canonical_source | 中文别名 | 命令层可用 | Schema 可用 |
|---|---|---|---|
| announcement | 公告 | ✓ | ✓ |
| news | 新闻 | ✓ | ✓ |
| market_anomaly | 交易异动 | ✓ | ✓ |
| filing_update | 文件更新/备案更新 | ✗ | ✓ |
| manual | 手动触发 | ✗ | ✓ |

### 层级关系

- **命令层 subset**：`announcement`, `news`, `market_anomaly` → 用于 `/risk-monitor-event-update`
- **Schema 全集**：以上 5 个 → 用于规则定义 `event_triggers[].source`

### 中文→英文映射

| 中文 | 英文 |
|---|---|
| 公告 | announcement |
| 新闻 | news |
| 异动 | market_anomaly |
| 文件更新 | filing_update |
| 手动触发 | manual |

