# 金融分析项目最佳实践

基于历史 `analysis_*` 项目的经验总结，帮助 AI 更高效地完成金融分析任务。

---

## 📋 常见错误和解决方案

### 1. API 调用错误

#### 错误 1.1：日期参数过时
```bash
# ❌ 错误：使用过时日期
--params '{"date": "2024-12-31"}'

# ✅ 正确：使用最近日期
--params '{"date": "2026-02-24"}'
--params '{"startDate": "2026-02-20"}'
```

**教训**：
- 永远使用最近的日期（当前月份或上个月）
- 避免使用超过3个月的历史日期
- 数据过时会导致分析结果无意义

#### 错误 1.2：API 路径格式错误
```bash
# ❌ 错误：使用点号
--suffix "cn.company.dividend"

# ✅ 正确：使用斜杠
--suffix "cn/company/dividend"
```

#### 错误 1.3：stockCodes 参数错误
```bash
# ❌ 错误：多个股票代码（某些 API 不支持）
--params '{"stockCodes": ["000300", "000905", "000852"]}'
# Error: "stockCodes" must contain 1 items

# ✅ 正确：单个查询或循环查询
for code in 000300 000905 000852; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ...
done
```

**教训**：
- 使用 API 前必须 grep 查看文档
- 确认 API 是否支持批量查询
- 某些 API（如 cn/index/fundamental）使用 startDate 时只能传一个代码

#### 错误 1.4：metricsList 参数错误
```bash
# ❌ 错误：使用不存在的指标
--params '{"metricsList": ["roe_ttm"]}'
# Error: (roe_ttm) are invalid price metrics

# ✅ 正确：查看 API 文档确认支持的指标
cat skills/lixinger-data-query/api_new/api-docs/cn_company_fundamental_non_financial.md
--params '{"metricsList": ["pe_ttm", "pb", "dyr"]}'
```

**教训**：
- 不同 API 支持的指标不同
- fundamental API 需要 metricsList
- fs（财务）API 需要不同的 metricsList

#### 错误 1.5：数据为空
```bash
# 查询结果为空，可能原因：
# 1. 日期参数错误（date 不存在数据）
# 2. 股票代码错误
# 3. API 路径错误

# 解决方案：使用 startDate + limit
--params '{"startDate": "2026-02-20", "limit": 1}'
```

---

### 2. 数据处理错误

#### 错误 2.1：CSV 数据追加时重复表头
```bash
# ❌ 错误：直接追加会包含表头
python3 query_tool.py ... >> data.csv
python3 query_tool.py ... >> data.csv  # 第二次会有重复表头

# ✅ 正确：使用 tail -n +2 跳过表头
python3 query_tool.py ... > data.csv  # 第一次
python3 query_tool.py ... | tail -n +2 >> data.csv  # 后续追加
```

#### 错误 2.2：数据文件路径错误
```bash
# ❌ 错误：忘记创建目录
python3 query_tool.py ... > data/stocks.csv
# Error: No such file or directory

# ✅ 正确：先创建目录
mkdir -p analysis_xxx/data
python3 query_tool.py ... > analysis_xxx/data/stocks.csv
```

---

### 3. 项目结构错误

#### 错误 3.1：没有创建项目文件夹
```bash
# ❌ 错误：直接在根目录操作
python3 query_tool.py ... > index_data.csv

# ✅ 正确：创建项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_主题"
mkdir -p ${PROJECT}/{data,output,scripts}
```

#### 错误 3.2：文件命名不规范
```bash
# ❌ 错误：文件名不清晰
data.csv
result.csv
output.md

# ✅ 正确：使用描述性文件名
data/index_valuation.csv
data/quality_stocks.csv
output/allocation_plan.md
```

---

## ✅ 最佳实践

### 1. 项目初始化流程

```bash
# 第一步：创建项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_主题关键词"
mkdir -p ${PROJECT}/{data,output,scripts}

# 第二步：创建 README.md
cat > ${PROJECT}/README.md << 'EOF'
# 项目标题

## 分析目标
[描述分析目标]

## 使用 Skills
- skills/China-market/xxx/

## 执行时间
$(date +%Y-%m-%d\ %H:%M:%S)

## 数据来源
- 理杏仁 API
- 分析日期：$(date +%Y-%m-%d)
EOF
```

### 2. 数据获取流程

```bash
# 第一步：grep 查看 API 文档（必须！）
cat skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md

# 第二步：确认参数格式
# - 使用斜杠而非点号
# - 确认是否支持批量查询
# - 确认 metricsList 支持的指标

# 第三步：执行查询（使用最近日期）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000300"], "startDate": "2026-02-20", "metricsList": ["pe_ttm.mcw", "pb.mcw"]}' \
  --limit 1 \
  > ${PROJECT}/data/index_valuation.csv

# 第四步：验证数据
cat ${PROJECT}/data/index_valuation.csv
```

### 3. 批量查询流程

```bash
# 方法 1：循环查询（推荐）
for code in 000300 000905 000852; do
  python3 query_tool.py \
    --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2026-02-20\"}" \
    ... | tail -n +2 >> data.csv  # 跳过表头
done

# 方法 2：先查询第一个（保留表头）
python3 query_tool.py --params '{"stockCodes": ["000300"]}' ... > data.csv
# 再查询其他（跳过表头）
for code in 000905 000852; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ... | tail -n +2 >> data.csv
done
```

### 4. 数据分析流程

```python
#!/usr/bin/env python3
"""
分析脚本模板
"""
import pandas as pd

def load_data():
    """加载数据"""
    try:
        df = pd.read_csv('data/xxx.csv')
        print(f"✅ 数据加载成功：{len(df)} 行")
        return df
    except FileNotFoundError:
        print("❌ 数据文件不存在")
        return None
    except Exception as e:
        print(f"❌ 数据加载失败：{e}")
        return None

def analyze_data(df):
    """分析数据"""
    if df is None or len(df) == 0:
        print("❌ 数据为空，无法分析")
        return
    
    # 数据清洗
    df['stockCode'] = df['stockCode'].astype(str).str.strip()
    
    # 分析逻辑
    for _, row in df.iterrows():
        code = row['stockCode']
        pe = row['pe_ttm.mcw']
        print(f"{code}: PE={pe:.2f}")

def main():
    """主函数"""
    print("=" * 70)
    print("数据分析报告")
    print("=" * 70)
    
    df = load_data()
    analyze_data(df)
    
    print("=" * 70)
    print("分析完成")
    print("=" * 70)

if __name__ == '__main__':
    main()
```

### 5. 报告生成流程

```bash
# 使用 fsWrite 创建报告
# 优点：
# - 一次性写入完整内容
# - 避免追加时的格式问题
# - 便于版本控制

# 报告结构：
# 1. 标题和元信息
# 2. 市场环境分析
# 3. 配置方案
# 4. 风险控制
# 5. 执行建议
# 6. 监控指标
```

---

## 📊 数据质量检查清单

### 查询前检查
- [ ] 已 grep 查看 API 文档
- [ ] 确认 API 路径格式（斜杠）
- [ ] 确认参数格式（stockCodes 单数/复数）
- [ ] 使用最近日期（2026-02-xx）
- [ ] 确认 metricsList 支持的指标

### 查询后检查
- [ ] 数据文件不为空
- [ ] 数据有表头
- [ ] 数据行数合理（>0）
- [ ] 数值字段无异常（非 NaN）
- [ ] 日期字段正确

### 分析前检查
- [ ] 数据文件路径正确
- [ ] 数据格式正确（CSV）
- [ ] 数据可以正常加载
- [ ] 数据字段完整

---

## 🔄 项目复用建议

### 1. 参考历史项目

**查找相似项目**：
```bash
# 查看所有历史项目
ls -d analysis_*

# 查看项目 README
cat analysis_xxx/README.md

# 查看项目脚本
ls analysis_xxx/scripts/
```

**可复用的项目**：
- `analysis_20260225_115511_portfolio_allocation/`：资产配置方案（100万）
- `analysis_20260225_141848_10m_portfolio/`：资产配置方案（1000万）
- `analysis_20260225_132632_aggressive_portfolio/`：积极型配置
- `analysis_20260225_114923_maotai_dividend/`：分红数据查询

### 2. 复用脚本

**数据获取脚本**：
```bash
# 复制脚本到新项目
cp analysis_xxx/scripts/01_fetch_index_valuation.sh ${PROJECT}/scripts/

# 修改参数
# - 更新日期
# - 更新股票代码
# - 更新输出路径
```

**分析脚本**：
```bash
# 复制 Python 分析脚本
cp analysis_xxx/scripts/04_comprehensive_analysis.py ${PROJECT}/scripts/

# 修改逻辑
# - 更新数据文件路径
# - 更新分析逻辑
# - 更新输出格式
```

### 3. 复用报告模板

**配置方案模板**：
```markdown
# 标题

## 一、市场环境分析
[指数估值、行业分析]

## 二、配置策略
[配置原则、配置结构]

## 三、具体配置方案
[详细配置表格]

## 四、风险控制要点
[风险识别、控制措施]

## 五、执行建议
[建仓策略、交易要点]

## 六、动态调整机制
[再平衡、止盈止损]

## 七、监控指标
[日/周/月/季度监控]
```

---

## 🎯 效率提升技巧

### 1. 使用 --columns 过滤字段

```bash
# ❌ 低效：返回所有字段（浪费 token）
python3 query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}'

# ✅ 高效：只返回需要的字段（节省 30-40% token）
python3 query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,cnName,industryName"
```

### 2. 使用 --limit 限制行数

```bash
# ❌ 低效：返回所有历史数据
python3 query_tool.py --params '{"startDate": "2020-01-01"}'

# ✅ 高效：只返回最近的数据
python3 query_tool.py --params '{"startDate": "2026-02-01"}' --limit 10
```

### 3. 使用 --row-filter 过滤数据

```bash
# ❌ 低效：查询后再过滤
python3 query_tool.py ... > data.csv
grep "条件" data.csv > filtered.csv

# ✅ 高效：查询时直接过滤
python3 query_tool.py ... --row-filter "dyr>0.05"
```

### 4. 批量操作使用脚本

```bash
# ❌ 低效：手动执行多次
python3 query_tool.py --params '{"stockCodes": ["600519"]}' ...
python3 query_tool.py --params '{"stockCodes": ["601318"]}' ...
python3 query_tool.py --params '{"stockCodes": ["600036"]}' ...

# ✅ 高效：使用循环
for code in 600519 601318 600036; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ...
done
```

---

## 📝 文档规范

### README.md 必备内容

```markdown
# 项目标题

## 分析目标
[明确的分析目标]

## 投资者画像（如适用）
- 资金规模
- 风险偏好
- 投资期限

## 使用 Skills
- skills/China-market/xxx/

## 执行时间
YYYY-MM-DD HH:MM:SS

## 数据来源
- 理杏仁 API
- 分析日期：YYYY-MM-DD

## 执行记录
### 数据文件
- data/xxx.csv: 说明

### 代码脚本
- scripts/xxx.sh: 说明

### 输出报告
- output/xxx.md: 说明

## 遇到的问题和解决方案
[记录错误和解决方法，便于后续参考]
```

### 报告文件命名规范

```
output/
├── allocation_plan.md        # 配置方案
├── action_checklist.md       # 执行清单
├── summary.md                # 一页总结
└── risk_analysis.md          # 风险分析
```

---

## 🚨 常见陷阱

### 1. 不要记忆 API 列表
```bash
# ❌ 错误：凭记忆使用 API
python3 query_tool.py --suffix "cn/company/xxx"

# ✅ 正确：每次都 grep 查看文档
grep -r "关键词" skills/lixinger-data-query/api_new/api-docs/
cat skills/lixinger-data-query/api_new/api-docs/xxx.md
```

### 2. 不要使用过时日期
```bash
# ❌ 错误：使用 2024 年日期（现在是 2026 年）
--params '{"date": "2024-12-31"}'

# ✅ 正确：使用最近日期
--params '{"date": "2026-02-25"}'
--params '{"startDate": "2026-02-01"}'
```

### 3. 不要忽略错误信息
```bash
# 如果查询失败，仔细阅读错误信息：
# - ValidationError: 参数格式错误
# - Api was not found: API 路径错误
# - invalid metrics: 指标不支持

# 根据错误信息调整参数，不要盲目重试
```

### 4. 不要过度查询
```bash
# ❌ 错误：查询大量历史数据
--params '{"startDate": "2010-01-01"}'  # 16年数据

# ✅ 正确：只查询需要的数据
--params '{"startDate": "2025-01-01"}' --limit 100
```

---

## 📚 学习资源

### 必读文档
1. `skills/lixinger-data-query/SKILL.md` - 数据查询工具总览
2. `skills/lixinger-data-query/LLM_USAGE_GUIDE.md` - LLM 使用指南
3. `skills/lixinger-data-query/EXAMPLES.md` - 查询示例
4. `.kiro/steering/lixinger-skills.md` - 金融分析技能包

### 参考项目
1. `analysis_20260225_115511_portfolio_allocation/` - 完整的配置方案流程
2. `analysis_20260225_141848_10m_portfolio/` - 大额资金配置
3. `analysis_20260225_132632_aggressive_portfolio/` - 积极型配置

### API 文档
```bash
# 查看所有 API 文档
ls skills/lixinger-data-query/api_new/api-docs/

# 常用 API
cat skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md
cat skills/lixinger-data-query/api_new/api-docs/cn_company_fundamental_non_financial.md
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md
```

---

## 🎓 总结

### 核心原则
1. **先 grep 后查询**：使用 API 前必须查看文档
2. **使用最近日期**：避免使用过时数据
3. **创建项目文件夹**：一个对话 = 一个项目
4. **记录执行过程**：README.md 记录问题和解决方案
5. **参考历史项目**：复用成功的脚本和模板

### 效率提升
1. 使用 `--columns` 过滤字段（节省 30-40% token）
2. 使用 `--limit` 限制行数
3. 使用循环批量查询
4. 复用历史项目的脚本

### 质量保证
1. 查询前检查参数格式
2. 查询后验证数据质量
3. 分析前检查数据完整性
4. 报告中记录数据来源和日期

---

**最后更新**：2026-02-25  
**维护者**：AI Assistant  
**用途**：指导 AI 更高效地完成金融分析任务
