---
test_type: smoke
command: "risk-monitor-scan"
target_skill: "risk-monitor-orchestrator"
created_at: "2026-04-12"
---

# Smoke Test Cases: risk-monitor-scan

## Case 1: 成功路径（legacy_only 模式）

### 输入参数
```json
{
  "watchlist": ["600519", "000858", "300750"],
  "mode": "legacy_only",
  "as_of_date": "2026-04-12"
}
```

### 预期输出
```json
{
  "dispatch_timestamp": "2026-04-12T12:00:00Z",
  "input": {
    "mode": "legacy_only",
    "watchlist": ["600519", "000858", "300750"],
    "as_of_date": "2026-04-12"
  },
  "status": "completed",
  "execution_plan": {
    "mode": "legacy_only",
    "skills_invoked": [
      "equity-pledge-risk-monitor",
      "goodwill-risk-monitor",
      "ipo-lockup-risk-monitor",
      "limit-up-limit-down-risk-checker",
      "liquidity-impact-estimator",
      "margin-risk-monitor",
      "shareholder-risk-check",
      "shareholder-structure-monitor",
      "st-delist-risk-scanner"
    ]
  },
  "results": {
    "summary": {
      "600519": {
        "overall_risk": "low",
        "action": "retain",
        "key_risks": []
      },
      "000858": {
        "overall_risk": "low",
        "action": "retain",
        "key_risks": []
      },
      "300750": {
        "overall_risk": "medium",
        "action": "monitor",
        "key_risks": ["liquidity_impact"]
      }
    }
  },
  "output_template": "post-selection-risk-clearance-output-template",
  "qa_status": "passed"
}
```

### 验证点
1. ✅ status 为 `completed`
2. ✅ skills_invoked 包含 9 个 legacy skills
3. ✅ 每只股票有 `overall_risk` 和 `action` 字段
4. ✅ qa_status 为 `passed`
5. ✅ output_template 符合约定

---

## Case 2: 降级路径（hybrid 模式 disagreement）

### 输入参数
```json
{
  "watchlist": ["600519"],
  "mode": "hybrid",
  "as_of_date": "2026-04-12"
}
```

### 预期输出
```json
{
  "dispatch_timestamp": "2026-04-12T12:00:00Z",
  "input": {
    "mode": "hybrid",
    "watchlist": ["600519"],
    "as_of_date": "2026-04-12"
  },
  "status": "completed_with_disagreement",
  "execution_plan": {
    "mode": "hybrid",
    "legacy_branch": "completed",
    "engine_branch": "completed"
  },
  "comparison": {
    "600519": {
      "legacy": {
        "equity_pledge": {
          "severity": "low",
          "thesis": "质押比例正常"
        }
      },
      "engine": {
        "PLEDGE_001": {
          "severity": "medium",
          "thesis": "质押比例接近阈值，需关注"
        }
      },
      "comparison_result": {
        "severity_gap": 1,
        "thesis_overlap": 0.6,
        "needs_review": false
      }
    }
  },
  "qa_status": "passed",
  "warnings": [
    "hybrid mode: 1 ticker has severity gap of 1 level"
  ]
}
```

### 验证点
1. ✅ status 为 `completed_with_disagreement` 或 `completed`
2. ✅ legacy_branch 和 engine_branch 都为 `completed`
3. ✅ comparison_result 包含 `severity_gap` 和 `thesis_overlap`
4. ✅ severity_gap ≤ 1 时 `needs_review` 为 false
5. ✅ qa_status 为 `passed`

---

## Case 3: 拒绝路径（无效参数）

### 输入参数
```json
{
  "watchlist": [],
  "mode": "invalid_mode",
  "as_of_date": "2026-04-12"
}
```

### 预期输出
```json
{
  "dispatch_timestamp": "2026-04-12T12:00:00Z",
  "input": {
    "mode": "invalid_mode",
    "watchlist": [],
    "as_of_date": "2026-04-12"
  },
  "status": "rejected",
  "errors": [
    {
      "field": "watchlist",
      "message": "watchlist must contain at least 1 ticker"
    },
    {
      "field": "mode",
      "message": "mode must be one of: legacy_only, hybrid, engine_only"
    }
  ],
  "qa_status": "failed_input_validation"
}
```

### 验证点
1. ✅ status 为 `rejected`
2. ✅ errors 数组包含字段级错误信息
3. ✅ watchlist 为空时拒绝执行
4. ✅ mode 无效时拒绝执行
5. ✅ qa_status 为 `failed_input_validation`

---

## Smoke Test 执行脚本

```bash
# 执行 Case 1
python3 skills/risk-monitor-orchestrator/dispatcher.py \
  --mode legacy_only \
  --watchlist '["600519","000858","300750"]' \
  --as-of-date 2026-04-12

# 执行 Case 2
python3 skills/risk-monitor-orchestrator/dispatcher.py \
  --mode hybrid \
  --watchlist '["600519"]' \
  --as-of-date 2026-04-12

# 执行 Case 3（预期失败）
python3 skills/risk-monitor-orchestrator/dispatcher.py \
  --mode invalid_mode \
  --watchlist '[]'
```