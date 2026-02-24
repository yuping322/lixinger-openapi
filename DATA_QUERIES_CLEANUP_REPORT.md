# Data Queries 精简优化报告

## 优化目标

根据用户反馈，对所有 China-market skills 的 `data-queries.md` 文件进行精简优化：
1. 去掉 Findata Service API 部分
2. 针对每个 skill 的具体需求定制化内容
3. 删除无用信息，保持精简

---

## 优化结果

### 文件大小对比

| 版本 | 文件大小 | 减少比例 |
|------|---------|---------|
| 优化前 | 7.6 KB | - |
| 优化后 | 0.8-1.0 KB | 87% ↓ |

### 更新统计

- **总文件数**: 56
- **成功更新**: 56
- **成功率**: 100%

---

## 优化内容

### 1. 去掉冗余部分

**删除内容**：
- ❌ Findata Service API 部分（不再使用）
- ❌ 理杏仁 API 直接调用示例（Python 代码）
- ❌ AKShare 替代数据源
- ❌ 数据限制说明
- ❌ 数据字段说明
- ❌ 最佳实践（已在主文档中）
- ❌ 技巧提示

**保留内容**：
- ✅ query_tool.py 查询示例（针对性定制）
- ✅ 参数说明（精简版）
- ✅ 查找更多 API 的方法

### 2. 针对性定制

根据每个 skill 的名称和特点，自动推断需要的 API 并生成对应示例：

| Skill 类型 | 推断的 API | 示例数量 |
|-----------|-----------|---------|
| dividend | cn.company.dividend, cn.company.allotment | 2 |
| shareholder | cn.company.shareholders-num, cn.company.majority-shareholders | 2 |
| block-deal | cn.company.block-deal, cn.company.candlestick | 2 |
| hot-rank | cn.company.hot | 1 |
| financial | cn.company.fs.non_financial | 1 |
| 默认 | cn.company, cn.company.candlestick | 2 |

### 3. 精简结构

**新结构**：
```
# 数据获取指南
├── 查询示例（1-2个针对性示例）
├── 参数说明（精简版）
└── 查找更多 API
```

**旧结构**：
```
# 数据获取指南
├── 推荐数据获取方式
│   ├── 理杏仁数据查询工具（详细）
│   ├── Findata Service API
│   └── 理杏仁 API 直接调用
├── 数据限制说明
├── 替代数据源
├── 数据字段说明
├── 最佳实践
├── 相关文档
└── 技巧提示
```

---

## 示例对比

### dividend-corporate-action-tracker

**优化前**（7.6 KB）：
- 包含 Findata Service API
- 包含 Python 代码示例
- 包含 AKShare 示例
- 包含数据字段说明
- 包含大量通用内容

**优化后**（1.0 KB）：
```markdown
# 数据获取指南

使用 `query_tool.py` 获取 dividend-corporate-action-tracker 所需的数据。

## 查询示例

### 查询配股信息
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.allotment" ...

### 查询分红数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.dividend" ...

## 参数说明
- --suffix: API 路径
- --params: JSON 格式参数
- --columns: 指定返回字段（推荐使用，节省 30-40% token）

## 查找更多 API
cat skills/lixinger-data-query/SKILL.md
```

---

## 定制化示例

### 1. dividend-corporate-action-tracker
- 查询配股信息
- 查询分红数据

### 2. shareholder-risk-check
- 查询股东人数
- 查询前十大股东

### 3. block-deal-monitor
- 查询大宗交易
- 查询K线数据

### 4. hot-rank-sentiment-monitor
- 查询热度数据

### 5. financial-statement-analyzer
- 查询财务数据

---

## 技术实现

### 自动推断逻辑

```python
SKILL_API_MAPPING = {
    "dividend": ["cn.company.dividend", "cn.company.allotment"],
    "shareholder": ["cn.company.shareholders-num", "cn.company.majority-shareholders"],
    "block-deal": ["cn.company.block-deal", "cn.company.candlestick"],
    "hot": ["cn.company.hot"],
    # ... 更多映射
}

def infer_apis(skill_name):
    """根据 skill 名称推断需要的 API"""
    apis = []
    for keyword, api_list in SKILL_API_MAPPING.items():
        if keyword in skill_name:
            apis.extend(api_list)
    
    if not apis:
        apis = ["cn.company", "cn.company.candlestick"]  # 默认
    
    return list(set(apis))
```

### API 示例库

为每个常用 API 预定义了精简的查询示例：
- 只包含最常用的参数
- 使用 `--columns` 过滤字段
- 使用 `--limit` 控制数量

---

## 优化效果

### 1. 文件大小

- **减少 87%**：从 7.6 KB 降至 0.8-1.0 KB
- **节省空间**：56 个文件共节省约 370 KB

### 2. 可读性

- **更清晰**：只包含相关内容
- **更聚焦**：针对性示例
- **更简洁**：去掉冗余信息

### 3. 维护性

- **自动化**：通过脚本生成，易于批量更新
- **一致性**：所有文件结构统一
- **可扩展**：易于添加新的 API 映射

### 4. LLM 友好

- **减少 token**：文件大小减少 87%
- **提高效率**：只读取需要的内容
- **降低成本**：减少 API 调用成本

---

## 备份说明

所有原始文件已备份为 `.bak3` 文件：
```bash
# 恢复单个文件
mv skills/China-market/dividend-corporate-action-tracker/references/data-queries.md.bak3 \
   skills/China-market/dividend-corporate-action-tracker/references/data-queries.md

# 批量恢复
find skills/China-market -name "data-queries.md.bak3" -type f | while read file; do
  mv "$file" "${file%.bak3}"
done
```

---

## 相关文件

### 生成脚本

1. **generate_minimal_data_queries.py**
   - 主生成脚本
   - 包含 API 映射和示例库
   - 自动推断和生成内容

2. **analyze_skills_data_needs.py**
   - 分析工具
   - 统计 API 使用频率

### 模板文件

1. **skills/China-market/DATA_QUERIES_TEMPLATE.md**
   - 新版精简模板
   - 0.8 KB

---

## 总结

本次优化成功实现了：

1. ✅ 去掉 Findata Service API 部分
2. ✅ 针对每个 skill 定制化内容
3. ✅ 删除无用信息，保持精简
4. ✅ 文件大小减少 87%
5. ✅ 所有 56 个文件更新成功

新版本的 data-queries.md 文件：
- 更精简（0.8-1.0 KB vs 7.6 KB）
- 更针对性（根据 skill 定制）
- 更易维护（自动化生成）
- 更 LLM 友好（减少 token 消耗）

---

**优化时间**: 2026-02-23  
**优化者**: Kiro AI  
**文档版本**: 2.0
