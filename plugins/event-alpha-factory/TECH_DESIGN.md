# Event Alpha Factory（Plugin C）技术设计

## 1. 目标

本插件用于把“事件检测”转为“可交易且可验证”的 alpha 研究流水线，核心链路：

**事件冲击 → 定价偏差 → 跟踪验证（1D/5D/20D）**。

它回答两个问题：

1. 哪些事件会形成可交易预期差？
2. 影响是一次性冲击，还是中期重估？

---

## 2. 插件定位（与已有技能协同）

本插件不替代 detector/study 技能，而是作为中间层工厂：

- 上游：接入事件来源（公告监控、财报反应、内部人交易等）
- 中游：统一 taxonomy + 事件研究 + 偏离度分位
- 下游：输出可执行验证任务与回填结果

建议接入：

- `*_event-driven-detector`
- `*_event-study`
- `US-market_us-earnings-reaction-analyzer`
- `China-market_disclosure-notice-monitor`
- `China-market_ipo-newlist-monitor`
- `China-market_ipo-lockup-risk-monitor`
- `China-market_share-repurchase-monitor`
- `*_insider-trading-analyzer`

---

## 3. 目录结构

```text
plugins/event-alpha-factory/
  TECH_DESIGN.md
  events/
    event_taxonomy.json
    post_event_playbook.json
    abnormal_return_panel.parquet      # 由计算任务生成
  schemas/
    abnormal_return_panel.schema.json
  scripts/
    score_event_alpha.py
    generate_post_event_checklist.py
```

---

## 4. 三个核心中间层

## 4.1 `events/event_taxonomy.json`

用途：统一事件分类，保证“当前事件 vs 历史同类”的可比性。

关键字段：

- `family`：业绩、资本行为、IPO、监管等
- `event_type`：如 `earnings_beat` / `share_repurchase`
- `direction`：利多/利空/中性
- `severity`：强/中/弱
- `mapping_rules`：来源文本到标准类型映射规则

## 4.2 `events/abnormal_return_panel.parquet`

用途：保存事件窗口异常收益面板，支持分位与偏离计算。

关键指标：

- `ar_1d`, `ar_5d`, `ar_20d`
- `pct_rank_1d`, `pct_rank_5d`, `pct_rank_20d`
- `zscore_1d`, `zscore_5d`, `zscore_20d`
- `confounder_flag`, `data_quality_score`

## 4.3 `events/post_event_playbook.json`

用途：为每种事件自动生成 1D/5D/20D 的验证清单，而不是只做摘要。

---

## 5. 处理流程（E2E）

1. 接收上游事件对象（symbol、event_time、raw_text、source_skill）
2. 用 taxonomy 做标准化分类（family/type/direction/severity）
3. 拉取历史同类样本并计算当前事件分位
4. 计算 `EventAlphaScore`
5. 基于 playbook 生成 1D/5D/20D 观察任务
6. T+1/T+5/T+20 回填验证结果，形成闭环反馈

---

## 6. 偏离度评分

示例：

`EventAlphaScore = 0.35*SurpriseStrength + 0.30*PersistenceProb + 0.20*Tradability - 0.15*ConfounderPenalty`

说明：

- `SurpriseStrength`：当前事件异常收益在同类历史分位
- `PersistenceProb`：历史同分位样本在 5D/20D 继续同向概率
- `Tradability`：流动性、点差、冲击成本约束
- `ConfounderPenalty`：同窗多事件干扰惩罚

---

## 7. MVP（两周）

首批覆盖：

- 财报超预期/不及预期
- 回购公告
- 解禁风险

交付：

- taxonomy v1（含规则）
- panel schema + 计算脚本
- playbook v1
- 评分与验证任务生成脚本

---

## 8. 验证标准

- 分位越高，后验收益单调性越清晰（校准）
- 高分事件在 5D/20D 命中率显著高于基线
- 验证任务完成率 > 95%，可回溯可复盘
