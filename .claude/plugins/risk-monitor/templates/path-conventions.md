# 路径规范说明

本文档定义 Risk Monitor Plugin 内所有组件的标准路径约定，确保迁移与开发过程中路径引用一致性。

---

## 1. Legacy Skills 路径

**旧能力迁移区**（仅迁移，不改造）

```
.claude/plugins/risk-monitor/skills/legacy/{skill-name}/
```

### 示例

- `.claude/plugins/risk-monitor/skills/legacy/equity-pledge-risk-monitor/`
- `.claude/plugins/risk-monitor/skills/legacy/shareholder-risk-check/`
- `.claude/plugins/risk-monitor/skills/legacy/goodwill-risk-monitor/`

### Legacy Skill 内部结构

```
skills/legacy/{skill-name}/
├── SKILL.md                    # Skill 定义文件
├── INSTALLATION.md            # 安装说明
├── DECISIONS.md               # 设计决策记录
└── references/
    ├── methodology.md         # 方法论说明
    ├── data-queries.md        # 数据查询示例
    └── output-template.md     # 输出模板
```

---

## 2. Risk Signal Engine 路径

**新规则引擎开发区**

```
.claude/plugins/risk-monitor/skills/risk-signal-engine/
```

### 规则文件路径

```
.claude/plugins/risk-monitor/skills/risk-signal-engine/rules/{rule-name}.json
```

### 示例

- `.claude/plugins/risk-monitor/skills/risk-signal-engine/rules/pledge_rules.json`
- `.claude/plugins/risk-monitor/skills/risk-signal-engine/rules/lockup_rules.json`
- `.claude/plugins/risk-monitor/skills/risk-signal-engine/rules/margin_rules.json`

---

## 3. Templates 路径

**模板与规范文档区**

```
.claude/plugins/risk-monitor/templates/
```

### 包含文件

- `capability-matrix-template.md` - 能力对照矩阵模板
- `post-selection-risk-clearance-output-template.md` - 排雷输出模板
- `path-conventions.md` - 路径规范说明（本文档）

---

## 4. Commands 路径

**命令入口区**

```
.claude/plugins/risk-monitor/commands/
```

### 包含文件

- `risk-monitor-scan.md` - 选股后排雷扫描命令
- `risk-monitor-event-update.md` - 持仓后事件更新命令

---

## 5. Orchestrator 路径

**编排层（后续接入）**

```
.claude/plugins/risk-monitor/skills/risk-monitor-orchestrator/
```

---

## 6. 路径引用原则

1. **绝对路径优先**：所有文档内路径示例使用从项目根开始的绝对路径
2. **无历史前缀**：legacy skill 名称不包含 `China-market_` 等历史前缀
3. **迁移不改造**：legacy skill 内部文档更新时仅修正路径，不改逻辑
4. **新开发独立**：新规则仅在 `risk-signal-engine` 内开发

---

## 7. 迁移前 vs 迁移后对照

| 类型 | 迁移前路径 | 迁移后路径 |
|------|-----------|-----------|
| Legacy Skill | `.claude/skills/China-market_{skill-name}/` | `.claude/plugins/risk-monitor/skills/legacy/{skill-name}/` |
| 规则文件 | 无独立规范 | `.claude/plugins/risk-monitor/skills/risk-signal-engine/rules/{rule-name}.json` |

---

## 8. 验证方法

使用 grep 搜索确认无历史路径残留：

```bash
# 搜索历史路径模式
grep -r ".claude/skills/China-market_" .claude/plugins/risk-monitor --include="*.md"
# 应返回空

# 搜索历史前缀模式
grep -r "China-market_" .claude/plugins/risk-monitor --include="*.md"
# 仅允许在迁移说明中出现
```