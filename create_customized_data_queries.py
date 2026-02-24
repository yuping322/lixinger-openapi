#!/usr/bin/env python3
"""
为每个 China-market skill 创建定制化的 data-queries.md 文件。
根据 skill 的名称和特点，提供针对性的数据查询示例。
"""

import os
from pathlib import Path

# 定义每个 skill 需要的数据类型和对应的查询示例
SKILL_DATA_MAPPING = {
    "dividend-corporate-action-tracker": {
        "apis": ["cn.company.dividend", "cn.company.allotment", "cn.company.equity-change"],
        "examples": [
            {
                "desc": "查询分红数据",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.dividend" --params \'{"stockCode": "600519"}\' --columns "date,dividendPerShare,dividendYield" --limit 20'
            },
            {
                "desc": "查询配股信息",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.allotment" --params \'{"stockCode": "600519"}\' --columns "date,allotmentRatio,allotmentPrice"'
            },
            {
                "desc": "查询股本变动",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.equity-change" --params \'{"stockCode": "600519"}\' --columns "date,changeReason,capitalization"'
            }
        ]
    },
    "shareholder-risk-check": {
        "apis": ["cn.company.shareholders-num", "cn.company.majority-shareholders", "cn.company.pledge"],
        "examples": [
            {
                "desc": "查询股东人数变化",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.shareholders-num" --params \'{"stockCode": "600519"}\' --columns "date,num,shareholdersNumberChangeRate" --limit 20'
            },
            {
                "desc": "查询前十大股东",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.majority-shareholders" --params \'{"stockCode": "600519"}\' --columns "date,shareholderName,holdingRatio"'
            }
        ]
    },
    "block-deal-monitor": {
        "apis": ["cn.company.block-deal", "cn.company.candlestick"],
        "examples": [
            {
                "desc": "查询大宗交易数据",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.block-deal" --params \'{"stockCode": "600519"}\' --columns "date,price,volume,premium" --limit 20'
            },
            {
                "desc": "查询K线数据（对比价格）",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.candlestick" --params \'{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}\' --columns "date,close,volume"'
            }
        ]
    },
    "bse-selection-analyzer": {
        "apis": ["cn.company", "cn.company.fundamental.non_financial", "cn.company.candlestick"],
        "examples": [
            {
                "desc": "筛选北交所股票",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params \'{}\' --row-filter \'{"exchange": {"==": "bj"}}\' --columns "stockCode,name,ipoDate"'
            },
            {
                "desc": "查询基本面数据",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.fundamental.non_financial" --params \'{"date": "2024-12-31", "stockCodes": ["430047"]}\' --columns "stockCode,pe_ttm,pb,marketValue"'
            }
        ]
    },
    # 默认配置（用于其他 skills）
    "default": {
        "apis": ["cn.company", "cn.company.candlestick", "cn.company.fundamental.non_financial"],
        "examples": [
            {
                "desc": "查询股票基本信息",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params \'{"stockCodes": ["600519"]}\' --columns "stockCode,name,ipoDate,exchange"'
            },
            {
                "desc": "查询K线数据",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.candlestick" --params \'{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}\' --columns "date,open,close,high,low,volume"'
            },
            {
                "desc": "查询基本面数据",
                "cmd": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.fundamental.non_financial" --params \'{"date": "2024-12-31", "stockCodes": ["600519"]}\' --columns "stockCode,pe_ttm,pb,marketValue"'
            }
        ]
    }
}

def generate_data_queries_content(skill_name):
    """为指定 skill 生成 data-queries.md 内容"""
    
    # 获取该 skill 的配置，如果没有则使用默认配置
    config = SKILL_DATA_MAPPING.get(skill_name, SKILL_DATA_MAPPING["default"])
    
    content = f"""# 数据获取指南

本文档说明如何获取 {skill_name} 所需的数据。

---

## 使用 query_tool.py 获取数据

**工具路径**: `skills/lixinger-data-query/scripts/query_tool.py`

### 核心优势

- ✅ 字段过滤 (`--columns`): 只返回需要的字段，节省 30-40% token
- ✅ 数据筛选 (`--row-filter`): 过滤符合条件的数据
- ✅ CSV 格式输出: 默认格式，最节省 token

---

## 常用查询示例

"""
    
    # 添加示例
    for i, example in enumerate(config["examples"], 1):
        content += f"""### {i}. {example['desc']}

```bash
{example['cmd']}
```

"""
    
    # 添加参数说明
    content += """---

## 参数说明

**必需参数**:
- `--suffix`: API 路径
- `--params`: JSON 格式参数

**增强参数（推荐使用）**:
- `--columns`: 指定返回字段，逗号分隔
- `--row-filter`: JSON 格式过滤条件
- `--limit`: 限制返回行数

**可选参数**:
- `--format`: 输出格式 `csv`（默认）、`json`、`text`

---

## 查找更多 API

**查看 API 列表**:
```bash
cat skills/lixinger-data-query/SKILL.md
```

**搜索关键字**:
```bash
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/
```

**查看 API 文档**:
```bash
cat skills/lixinger-data-query/api_new/api-docs/<api_name>.md
```

---

## 相关文档

- **查询工具**: `skills/lixinger-data-query/SKILL.md`
- **使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **API 文档**: `skills/lixinger-data-query/api_new/api-docs/`
"""
    
    return content

def main():
    """主函数"""
    china_market_dir = Path("skills/China-market")
    
    # 查找所有包含 references/data-queries.md 的 skill 目录
    skill_dirs = []
    for skill_dir in china_market_dir.iterdir():
        if skill_dir.is_dir():
            data_queries_file = skill_dir / "references" / "data-queries.md"
            if data_queries_file.exists():
                skill_dirs.append(skill_dir)
    
    print(f"找到 {len(skill_dirs)} 个 skills")
    
    # 为每个 skill 生成定制化内容
    updated_count = 0
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        data_queries_file = skill_dir / "references" / "data-queries.md"
        
        # 生成内容
        content = generate_data_queries_content(skill_name)
        
        # 备份原文件
        backup_file = data_queries_file.with_suffix(".md.bak2")
        if data_queries_file.exists():
            import shutil
            shutil.copy2(data_queries_file, backup_file)
        
        # 写入新内容
        with open(data_queries_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        updated_count += 1
        print(f"✅ 更新: {skill_name}")
    
    print(f"\n{'='*60}")
    print(f"完成！共更新 {updated_count} 个文件")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
