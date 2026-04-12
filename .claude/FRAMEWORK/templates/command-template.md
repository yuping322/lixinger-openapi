---
description: "[一句话描述该命令的功能，不超过50字]"
argument-hint: "[参数说明，格式：--key1=value1 --key2=value2]"
target-skill: "[调用的 skill 名称]"
output-format: "markdown | json | table"
risk-level: "low | medium | high"
---

# [Command Name]

## 参数解析
- **参数1**: `{{args.key1}}`
  - 类型：[string | number | date]
  - 必填：[是/否]
  - 说明：[参数说明]
  - 默认值：[如有]

- **参数2**: `{{args.key2}}`
  - 类型：[string | number | date]
  - 必填：[是/否]
  - 说明：[参数说明]
  - 默认值：[如有]

## 调用 Skill
调用 `[skill-name]`，传入以下参数：
- `input_field_1`: `{{args.key1}}`
- `input_field_2`: `{{args.key2}}`

## 输出模板
按 `[output-template-name]` 格式输出结果：
- 输出格式：[markdown | json | table]
- 输出模板路径：`templates/[output-template-name].md`

## 错误处理
### REFUSE 场景
当 skill 返回 REFUSE 时：
- 输出错误提示："[具体错误提示信息]"
- 停止执行，不返回任何结果

### DOWNGRADE 场景
当 skill 返回 DOWNGRADE 时：
- 输出降级提示："部分数据缺失，置信度已降低"
- 继续输出结果，但标注置信度降低原因
- 在输出中添加 `⚠️ 降级警告` 标识

### 其他错误场景
- 参数缺失：返回 "缺少必填参数：[参数名]"
- 参数格式错误：返回 "参数格式错误：[参数名] 应为 [正确格式]"
- skill 调用失败：返回 "Skill [skill-name] 调用失败：[错误原因]"

## 示例用法
```bash
# 示例1：基本用法
/[command-name] --key1=value1 --key2=value2

# 示例2：使用默认值
/[command-name] --key1=value1

# 示例3：完整参数
/[command-name] --key1=value1 --key2=value2 --key3=value3
```

## 注意事项
- [注意事项1]
- [注意事项2]
- [相关限制或约束]