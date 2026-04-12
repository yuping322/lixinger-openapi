# [Orchestrator Name]

## 能力定义
[一句话描述该 orchestrator 的核心能力，不超过100字]

## 调度流程（Workflow）

### 流程图
```
[开始]
  ↓
[步骤1: 调用 skill-A]
  ↓
[步骤2: 调用 skill-B]
  ↓
[步骤3: 调用 skill-C]
  ↓
[步骤4: 执行 QA 校验]
  ↓
[步骤5: 汇总置信度]
  ↓
[结束]
```

### 详细流程

#### 步骤1：调用 skill-A 获取数据
- **Skill 名称**：`[skill-A-name]`
- **传入参数**：
  ```json
  {
    "param1": "{{input.field1}}",
    "param2": "{{input.field2}}"
  }
  ```
- **预期输出**：
  ```json
  {
    "result1": "value1",
    "result2": "value2",
    "confidence": 0.85
  }
  ```
- **失败处理**：
  - 如果 skill-A 返回 REFUSE → [处理动作]
  - 如果 skill-A 返回 DOWNGRADE → [处理动作]

#### 步骤2：调用 skill-B 进行分析
- **Skill 名称**：`[skill-B-name]`
- **传入参数**：
  ```json
  {
    "param1": "{{skill-A.result1}}",
    "param2": "{{input.field3}}"
  }
  ```
- **预期输出**：
  ```json
  {
    "analysis_result": "value",
    "confidence": 0.90
  }
  ```
- **失败处理**：
  - 如果 skill-B 返回 REFUSE → [处理动作]
  - 如果 skill-B 返回 DOWNGRADE → [处理动作]

#### 步骤3：调用 skill-C 生成结论
- **Skill 名称**：`[skill-C-name]`
- **传入参数**：
  ```json
  {
    "data": "{{skill-A.result1}}",
    "analysis": "{{skill-B.analysis_result}}"
  }
  ```
- **预期输出**：
  ```json
  {
    "conclusion": "final_value",
    "confidence": 0.88
  }
  ```
- **失败处理**：
  - 如果 skill-C 返回 REFUSE → [处理动作]
  - 如果 skill-C 返回 DOWNGRADE → [处理动作]

#### 步骤4：执行 QA 校验
- **校验规则**：见"QA 规则"部分
- **校验失败处理**：
  - 如果校验失败 → 执行降级策略
  - 如果校验通过 → 继续下一步

#### 步骤5：汇总置信度
- **汇总方式**：见"置信度汇总"部分
- **输出格式**：
  ```json
  {
    "result": "final_output",
    "total_confidence": 0.87,
    "data_gaps": [],
    "qa_status": "PASSED"
  }
  ```

## QA 规则（QA Rules）

| 规则名 | 校验内容 | 失败动作 | 失败提示 |
|-------|---------|---------|---------|
| cross_skill_consistency | skills A/B/C 输出一致性校验 | DOWNGRADE | "Skills 输出不一致，置信度已降低" |
| data_freshness | 数据时效性校验（数据时间 < [X] 小时） | REFUSE | "数据过期，请刷新数据源" |
| confidence_threshold | 总置信度 > 0.7 | WARNING | "置信度较低，结果仅供参考" |
| completeness_check | 必填字段完整性校验 | REFUSE | "缺少必填字段：[字段名]" |
| format_validation | 输出格式校验 | REFUSE | "输出格式错误" |

### QA 规则详细说明

#### 规则1：cross_skill_consistency（跨 Skill 一致性）
- **校验内容**：skills A/B/C 的输出是否存在逻辑冲突
- **校验条件**：
  ```python
  # 示例：skill-A 输出的估值区间应包含 skill-C 的最终估值
  skill_A.range_min <= skill_C.final_value <= skill_A.range_max
  ```
- **失败动作**：DOWNGRADE
- **失败提示**："Skills 输出不一致，置信度已降低：[不一致详情]"

#### 规则2：data_freshness（数据时效性）
- **校验内容**：检查数据的时效性
- **校验条件**：
  ```python
  # 示例：数据时间戳应在最近 24 小时内
  current_time - data_timestamp < 24 * 3600
  ```
- **失败动作**：REFUSE
- **失败提示**："数据过期（已超过 24 小时），请刷新数据源"

#### 规则3：confidence_threshold（置信度阈值）
- **校验内容**：总置信度是否达到最低阈值
- **校验条件**：
  ```python
  total_confidence >= 0.7
  ```
- **失败动作**：WARNING
- **失败提示**："置信度较低（[confidence]），结果仅供参考"

#### 规则4：completeness_check（完整性检查）
- **校验内容**：必填字段是否完整
- **校验条件**：
  ```python
  # 示例：检查必填字段是否为空
  all(required_field is not None for required_field in [field1, field2, field3])
  ```
- **失败动作**：REFUSE
- **失败提示**："缺少必填字段：[字段名]"

#### 规则5：format_validation（格式校验）
- **校验内容**：输出格式是否符合规范
- **校验条件**：
  ```python
  # 示例：检查 JSON 格式是否正确
  validate_json_schema(output, output_schema)
  ```
- **失败动作**：REFUSE
- **失败提示**："输出格式错误：[错误详情]"

## 降级策略（Fallback）

### 主 Skill 失败降级
- **skill-A 失败**：
  - 尝试备用 skill：`[skill-A-backup-name]`
  - 如果备用 skill 也失败 → REFUSE
  - 用户提示："主数据源失败，已切换至备用数据源，置信度可能降低"

- **skill-B 失败**：
  - 尝试简化分析：`[skill-B-simplified-name]`
  - 如果简化分析也失败 → REFUSE
  - 用户提示："完整分析失败，已使用简化分析，结果精度可能降低"

- **skill-C 失败**：
  - 尝试规则生成：`[rule-based-generator]`
  - 如果规则生成也失败 → REFUSE
  - 用户提示："智能生成失败，已使用规则生成，结果可能不够精准"

### 全局降级策略
- **所有 skill 失败**：
  - 动作：REFUSE
  - 用户提示："所有处理流程均失败，无法生成结果，请稍后重试或联系支持"

- **置信度 < 0.5**：
  - 动作：WARNING + 降级输出
  - 用户提示："结果置信度过低（[confidence]），建议谨慎使用"

- **部分数据缺失**：
  - 动作：DOWNGRADE
  - 用户提示："部分数据缺失（[缺失内容]），已使用替代方案，置信度已调整"

### 降级优先级
1. **最高优先级**：数据完整性（必须保证）
2. **高优先级**：核心计算逻辑（尽量保证）
3. **中优先级**：分析深度（可降级）
4. **低优先级**：辅助功能（可省略）

## 置信度汇总（Confidence Aggregation）

### 汇总公式
```python
total_confidence = (
    skill_A.confidence * 0.4 +  # skill-A 权重 40%
    skill_B.confidence * 0.3 +  # skill-B 权重 30%
    skill_C.confidence * 0.3    # skill-C 权重 30%
) * qa_multiplier  # QA 校验通过率调整系数
```

### QA 调整系数
```python
qa_multiplier = 1.0  # 初始值

# 根据 QA 规则结果调整
if cross_skill_consistency_passed:
    qa_multiplier *= 1.0
else:
    qa_multiplier *= 0.8  # 一致性校验失败，降低 20%

if data_freshness_passed:
    qa_multiplier *= 1.0
else:
    qa_multiplier *= 0.7  # 时效性校验失败，降低 30%

if confidence_threshold_passed:
    qa_multiplier *= 1.0
else:
    qa_multiplier *= 0.9  # 置信度阈值未达标，降低 10%

# 最终置信度不得低于 0
total_confidence = max(0, total_confidence)
```

### 权重分配依据
- **skill-A（40%）**：[权重分配理由]
- **skill-B（30%）**：[权重分配理由]
- **skill-C（30%）**：[权重分配理由]

### 置信度分级
- **高置信度（>= 0.8）**：结果可信度高，可放心使用
- **中等置信度（0.6 - 0.8）**：结果可用，但需注意可能存在的偏差
- **低置信度（0.5 - 0.6）**：结果仅供参考，建议交叉验证
- **极低置信度（< 0.5）**：结果不可靠，建议不要使用

## 输出格式（Output Format）

### 标准输出
```json
{
  "result": {
    "field1": "value1",
    "field2": "value2",
    "field3": "value3"
  },
  "total_confidence": 0.87,
  "data_gaps": [
    "缺失 [缺失内容]"
  ],
  "qa_status": "PASSED",
  "qa_details": {
    "cross_skill_consistency": true,
    "data_freshness": true,
    "confidence_threshold": true,
    "completeness_check": true,
    "format_validation": true
  },
  "fallback_used": false,
  "fallback_reason": null
}
```

### 降级输出
```json
{
  "result": {
    "field1": "value1",
    "field2": "value2_partial",
    "field3": "value3"
  },
  "total_confidence": 0.65,
  "data_gaps": [
    "缺失 [缺失内容]",
    "skill-B 使用了简化分析"
  ],
  "qa_status": "WARNING",
  "qa_details": {
    "cross_skill_consistency": false,
    "data_freshness": true,
    "confidence_threshold": false,
    "completeness_check": true,
    "format_validation": true
  },
  "fallback_used": true,
  "fallback_reason": "skill-B 完整分析失败，已使用简化分析"
}
```

### 拒绝输出
```json
{
  "error": "REFUSE",
  "message": "数据源不可用，请稍后重试",
  "total_confidence": 0,
  "qa_status": "FAILED",
  "qa_details": {
    "cross_skill_consistency": false,
    "data_freshness": false,
    "confidence_threshold": false,
    "completeness_check": false,
    "format_validation": false
  }
}
```

## 性能指标
- **预期响应时间**：[XX] 秒（包含所有 skill 调用）
- **最大并发数**：[XX] 个请求
- **超时设置**：[XX] 秒
- **重试策略**：最多重试 [X] 次，间隔 [X] 秒

## 版本历史
- **v1.0.0** ([日期])：初始版本
- **v1.1.0** ([日期])：[更新内容]