# [Skill Name]

## 能力定义
[一句话描述该 skill 的核心能力，不超过100字]

## 输入字段（Input Schema）
| 字段名 | 类型 | 必填 | 说明 | 示例值 |
|-------|------|-----|------|--------|
| [field1] | [string/number/date/array/object] | 是/否 | [字段说明] | [示例值] |
| [field2] | [string/number/date/array/object] | 是/否 | [字段说明] | [示例值] |
| [field3] | [string/number/date/array/object] | 是/否 | [字段说明] | [示例值] |

### 字段详细说明
**[field1]**：
- 类型：[string/number/date/array/object]
- 必填：[是/否]
- 说明：[详细说明]
- 验证规则：[格式要求、取值范围等]
- 示例值：`[example_value]`

**[field2]**：
- 类型：[string/number/date/array/object]
- 必填：[是/否]
- 说明：[详细说明]
- 验证规则：[格式要求、取值范围等]
- 示例值：`[example_value]`

## 输出字段（Output Schema）
| 字段名 | 类型 | 必填 | 说明 | 示例值 |
|-------|------|-----|------|--------|
| [result1] | [string/number/array/object] | 是/否 | [字段说明] | [示例值] |
| [result2] | [string/number/array/object] | 是/否 | [字段说明] | [示例值] |
| confidence | float | 是 | 置信度 [0, 1] | 0.85 |
| data_gap | string | 否 | 数据缺口说明 | null |

### 输出字段详细说明
**[result1]**：
- 类型：[string/number/array/object]
- 必填：[是/否]
- 说明：[详细说明]
- 计算逻辑：[简要说明计算方法]
- 示例值：`[example_value]`

**confidence**：
- 类型：float
- 必填：是
- 说明：结果置信度，取值范围 [0, 1]
- 计算方式：见"置信度来源"部分
- 示例值：`0.85`

**data_gap**：
- 类型：string
- 必填：否
- 说明：当存在数据缺失时的说明信息，无缺失时为 null
- 示例值：`"缺少2024年Q4财报数据"`

## 失败模式（Failure Modes）
| 失败类型 | 触发条件 | 降级行为 | 用户提示 |
|---------|---------|---------|---------|
| DATA_NOT_AVAILABLE | 数据源无响应或数据缺失 | REFUSE | "数据源暂时不可用，请稍后重试" |
| INVALID_INPUT | 输入参数格式错误或不合法 | REFUSE | "参数 [param] 格式错误，应为 [正确格式]" |
| PARTIAL_DATA | 部分数据缺失但可继续计算 | DOWNGRADE | "部分数据缺失，置信度已降低：[缺失内容]" |
| COMPUTATION_ERROR | 计算过程出错 | REFUSE | "计算过程出错：[错误详情]" |
| TIMEOUT | 处理超时 | REFUSE | "处理超时，请稍后重试" |

### 失败类型详细说明
**DATA_NOT_AVAILABLE**：
- 触发场景：[具体场景说明]
- 检测方式：[如何检测该失败]
- 降级行为：REFUSE（拒绝执行）
- 用户提示："数据源暂时不可用，请稍后重试"

**PARTIAL_DATA**：
- 触发场景：[具体场景说明]
- 检测方式：[如何检测该失败]
- 降级行为：DOWNGRADE（降级执行）
- 用户提示："部分数据缺失，置信度已降低：[缺失内容]"

## 置信度来源（Confidence Source）
### 置信度计算公式
```
confidence = w1 * c1 + w2 * c2 + w3 * c3 + ...
```

### 权重分配
- **数据完整性（c1）**：权重 [XX]%
  - 说明：[如何评估数据完整性]
  - 计算方式：[具体计算方法]

- **计算稳定性（c2）**：权重 [XX]%
  - 说明：[如何评估计算稳定性]
  - 计算方式：[具体计算方法]

- **[其他来源]（c3）**：权重 [XX]%
  - 说明：[说明]
  - 计算方式：[具体计算方法]

### 置信度阈值
- **高置信度**：confidence >= 0.8 → 结果可信
- **中等置信度**：0.5 <= confidence < 0.8 → 结果可用但需注意
- **低置信度**：confidence < 0.5 → 建议降级或拒绝

## 最小示例（Minimal Example）

### 示例1：正常场景
**输入**：
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**输出**：
```json
{
  "result1": "output_value1",
  "result2": "output_value2",
  "confidence": 0.85,
  "data_gap": null
}
```

### 示例2：部分数据缺失（DOWNGRADE）
**输入**：
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**输出**：
```json
{
  "result1": "output_value1",
  "result2": "output_value2_partial",
  "confidence": 0.65,
  "data_gap": "缺少 [缺失内容] 数据"
}
```

### 示例3：数据不可用（REFUSE）
**输入**：
```json
{
  "field1": "invalid_value",
  "field2": "value2"
}
```

**输出**：
```json
{
  "error": "DATA_NOT_AVAILABLE",
  "message": "数据源暂时不可用，请稍后重试",
  "confidence": 0
}
```

## QA 规则（QA Rules）

### 数据质量规则
- **规则1**：[字段名] 必须在 [范围] 内
  - 校验条件：[具体校验逻辑]
  - 失败动作：REFUSE

- **规则2**：[字段名] 格式必须符合 [格式要求]
  - 校验条件：[具体校验逻辑]
  - 失败动作：REFUSE

### 计算一致性规则
- **规则3**：[计算结果] 必须在 [合理范围] 内
  - 校验条件：[具体校验逻辑]
  - 失败动作：DOWNGRADE

- **规则4**：[字段A] 与 [字段B] 的关系必须满足 [条件]
  - 校验条件：[具体校验逻辑]
  - 失败动作：WARNING

### 输出完整性规则
- **规则5**：必填字段不能为空或 null
  - 校验条件：[具体校验逻辑]
  - 失败动作：REFUSE

- **规则6**：confidence 必须在 [0, 1] 区间
  - 校验条件：`confidence >= 0 && confidence <= 1`
  - 失败动作：REFUSE

## 依赖关系
- **数据依赖**：[依赖的数据源或数据集]
- **工具依赖**：[依赖的工具或函数]
- **其他 Skill 依赖**：[依赖的其他 skills]

## 性能指标
- **预期响应时间**：[XX] 秒
- **最大数据量**：[XX] 条记录
- **并发支持**：[是/否]

## 版本历史
- **v1.0.0** ([日期])：初始版本
- **v1.1.0** ([日期])：[更新内容]