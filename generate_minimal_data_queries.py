#!/usr/bin/env python3
"""生成精简的、针对性的 data-queries.md 文件"""

from pathlib import Path
import re

# API 示例映射
API_EXAMPLES = {
    "cn.company": {
        "desc": "查询股票基本信息",
        "cmd": '--suffix "cn.company" --params \'{"stockCodes": ["600519"]}\' --columns "stockCode,name,ipoDate"'
    },
    "cn.company.candlestick": {
        "desc": "查询K线数据",
        "cmd": '--suffix "cn.company.candlestick" --params \'{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}\' --columns "date,close,volume"'
    },
    "cn.company.dividend": {
        "desc": "查询分红数据",
        "cmd": '--suffix "cn.company.dividend" --params \'{"stockCode": "600519"}\' --columns "date,dividendPerShare,dividendYield" --limit 20'
    },
    "cn.company.allotment": {
        "desc": "查询配股信息",
        "cmd": '--suffix "cn.company.allotment" --params \'{"stockCode": "600519"}\' --columns "date,allotmentRatio,allotmentPrice"'
    },
    "cn.company.shareholders-num": {
        "desc": "查询股东人数",
        "cmd": '--suffix "cn.company.shareholders-num" --params \'{"stockCode": "600519"}\' --columns "date,num,shareholdersNumberChangeRate" --limit 20'
    },
    "cn.company.majority-shareholders": {
        "desc": "查询前十大股东",
        "cmd": '--suffix "cn.company.majority-shareholders" --params \'{"stockCode": "600519"}\' --columns "date,shareholderName,holdingRatio"'
    },
    "cn.company.block-deal": {
        "desc": "查询大宗交易",
        "cmd": '--suffix "cn.company.block-deal" --params \'{"stockCode": "600519"}\' --columns "date,price,volume,premium" --limit 20'
    },
    "cn.company.pledge": {
        "desc": "查询股权质押",
        "cmd": '--suffix "cn.company.pledge" --params \'{"stockCode": "600519"}\' --columns "date,pledgeRatio"'
    },
    "cn.company.announcement": {
        "desc": "查询公告",
        "cmd": '--suffix "cn.company.announcement" --params \'{"stockCode": "600519"}\' --columns "date,linkText,types" --limit 20'
    },
    "cn.company.equity-change": {
        "desc": "查询股本变动",
        "cmd": '--suffix "cn.company.equity-change" --params \'{"stockCode": "600519"}\' --columns "date,changeReason,capitalization"'
    },
    "cn.company.fundamental.non_financial": {
        "desc": "查询基本面数据",
        "cmd": '--suffix "cn.company.fundamental.non_financial" --params \'{"date": "2024-12-31", "stockCodes": ["600519"]}\' --columns "stockCode,pe_ttm,pb,marketValue"'
    },
    "cn.company.fs.non_financial": {
        "desc": "查询财务数据",
        "cmd": '--suffix "cn.company.fs.non_financial" --params \'{"stockCode": "600519"}\' --columns "date,revenue,netProfit,roe"'
    },
    "cn.company.trading-abnormal": {
        "desc": "查询龙虎榜",
        "cmd": '--suffix "cn.company.trading-abnormal" --params \'{"stockCode": "600519"}\' --columns "date,buyAmount,sellAmount"'
    },
    "cn.company.senior-executive-shares-change": {
        "desc": "查询高管增减持",
        "cmd": '--suffix "cn.company.senior-executive-shares-change" --params \'{"stockCode": "600519"}\' --columns "date,name,changeAmount"'
    },
    "cn.company.major-shareholders-shares-change": {
        "desc": "查询大股东增减持",
        "cmd": '--suffix "cn.company.major-shareholders-shares-change" --params \'{"stockCode": "600519"}\' --columns "date,shareholderName,changeAmount"'
    },
    "cn.company.margin-trading-and-securities-lending": {
        "desc": "查询融资融券",
        "cmd": '--suffix "cn.company.margin-trading-and-securities-lending" --params \'{"stockCode": "600519"}\' --columns "date,marginBalance,shortBalance"'
    },
    "cn.company.hot": {
        "desc": "查询热度数据",
        "cmd": '--suffix "cn.company.hot" --params \'{"stockCode": "600519"}\' --columns "date,hotRank"'
    },
    "cn.index": {
        "desc": "查询指数信息",
        "cmd": '--suffix "cn.index" --params \'{"stockCodes": ["000016"]}\' --columns "stockCode,name"'
    },
    "cn.index.constituents": {
        "desc": "查询指数成分股",
        "cmd": '--suffix "cn.index.constituents" --params \'{"date": "2024-12-31", "stockCodes": ["000016"]}\' --flatten "constituents" --columns "stockCode,weight"'
    },
    "cn.industry": {
        "desc": "查询行业信息",
        "cmd": '--suffix "cn.industry" --params \'{}\' --columns "industryCode,industryName"'
    },
    "cn.fund": {
        "desc": "查询基金信息",
        "cmd": '--suffix "cn.fund" --params \'{"stockCodes": ["110022"]}\' --columns "stockCode,name"'
    },
    "cn.fund.shareholdings": {
        "desc": "查询基金持仓",
        "cmd": '--suffix "cn.fund.shareholdings" --params \'{"stockCode": "110022"}\' --columns "date,stockCode,holdingRatio"'
    },
    "macro": {
        "desc": "查询宏观数据",
        "cmd": '--suffix "macro.gdp" --params \'{}\' --columns "date,value"'
    }
}

# 根据 skill 名称推断需要的 API
SKILL_API_MAPPING = {
    "dividend": ["cn.company.dividend", "cn.company.allotment"],
    "shareholder": ["cn.company.shareholders-num", "cn.company.majority-shareholders"],
    "block-deal": ["cn.company.block-deal", "cn.company.candlestick"],
    "pledge": ["cn.company.pledge"],
    "announcement": ["cn.company.announcement"],
    "fund": ["cn.fund", "cn.fund.shareholdings"],
    "index": ["cn.index", "cn.index.constituents"],
    "industry": ["cn.industry"],
    "macro": ["macro"],
    "margin": ["cn.company.margin-trading-and-securities-lending"],
    "dragon-tiger": ["cn.company.trading-abnormal"],
    "valuation": ["cn.company.fundamental.non_financial"],
    "financial": ["cn.company.fs.non_financial"],
    "insider": ["cn.company.senior-executive-shares-change", "cn.company.major-shareholders-shares-change"],
    "equity": ["cn.company.equity-change"],
    "hot": ["cn.company.hot"],
}

def infer_apis(skill_name):
    """根据 skill 名称推断需要的 API"""
    apis = []
    for keyword, api_list in SKILL_API_MAPPING.items():
        if keyword in skill_name:
            apis.extend(api_list)
    
    # 如果没有匹配，使用默认
    if not apis:
        apis = ["cn.company", "cn.company.candlestick"]
    
    return list(set(apis))

def generate_content(skill_name, apis):
    """生成 data-queries.md 内容"""
    content = f"""# 数据获取指南

使用 `query_tool.py` 获取 {skill_name} 所需的数据。

---

## 查询示例

"""
    
    # 添加示例
    for api in apis:
        if api in API_EXAMPLES:
            example = API_EXAMPLES[api]
            content += f"""### {example['desc']}

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py {example['cmd']}
```

"""
    
    # 添加参数说明
    content += """---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 查找更多 API

```bash
# 查看 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
"""
    
    return content

def main():
    """主函数"""
    china_market_dir = Path("skills/China-market")
    
    # 查找所有 skill 目录
    skill_dirs = []
    for skill_dir in china_market_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            data_queries_file = skill_dir / "references" / "data-queries.md"
            if data_queries_file.exists():
                skill_dirs.append(skill_dir)
    
    print(f"找到 {len(skill_dirs)} 个 skills")
    
    # 为每个 skill 生成内容
    updated_count = 0
    for skill_dir in sorted(skill_dirs):
        skill_name = skill_dir.name
        data_queries_file = skill_dir / "references" / "data-queries.md"
        
        # 推断需要的 API
        apis = infer_apis(skill_name)
        
        # 生成内容
        content = generate_content(skill_name, apis)
        
        # 备份原文件
        backup_file = data_queries_file.with_suffix(".md.bak3")
        import shutil
        shutil.copy2(data_queries_file, backup_file)
        
        # 写入新内容
        with open(data_queries_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        updated_count += 1
        print(f"✅ {skill_name}: {len(apis)} APIs")
    
    print(f"\n完成！共更新 {updated_count} 个文件")

if __name__ == "__main__":
    main()
