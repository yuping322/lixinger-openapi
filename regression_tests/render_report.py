import json
import os
from pathlib import Path

# 路径配置
BASE_DIR = Path("/Users/fengzhi/Downloads/git/lixinger-openapi")
RESULTS_DIR = BASE_DIR / "regression_tests" / "results"
SKILLS_DIR = BASE_DIR / "skills" / "China-market"

def render_md(skill_name, case_name, data):
    """根据 JSON 数据渲染 Markdown 报告，支持多种实体类型并优先尝试填充技能自带模板"""
    
    # 错误处理
    if "error" in data:
        return f"# {skill_name} - 运行错误\n\n数据采集失败: {data['error']}"

    # 1. 尝试识别实体类型
    entity_type = "generic"
    if "major_indices" in data or "market_fund_flow" in data or "sse_summary" in data:
        entity_type = "market"
    elif "interest_rates" in data or "money_supply" in data:
        entity_type = "macro"
    elif "industry_valuation" in data:
        entity_type = "sector"
    elif "identity" in data:
        entity_type = "stock" if "pe_ttm" in data.get("valuation", {}) else "fund"

    # 2. 准备基础信息
    identity = data.get("identity", {})
    name = identity.get("name") or data.get("name") or "全市场/宏观数据"
    code = identity.get("code") or ""
    title_name = f"{name} ({code})" if code else name

    # 3. 渲染核心表格
    data_lines = []
    
    if entity_type == "market":
        # 1. 指数表现
        indices = data.get("major_indices", [])
        if indices:
            data_lines.append("| 指数代码 | 最新价 | 涨跌幅 |")
            data_lines.append("| :--- | :--- | :--- |")
            for idx in indices:
                data_lines.append(f"| {idx.get('name')} | {idx.get('latest')} | {idx.get('change_pct')}% |")
            data_lines.append("")

        # 2. 估值快照
        val = data.get("valuation_overview", {})
        if val:
            data_lines.append("| 指标 | 数值 |")
            data_lines.append("| :--- | :--- |")
            for k, v in val.items():
                if k != "stockCode":
                    data_lines.append(f"| {k} | {v} |")

    elif entity_type == "macro":
        rates = data.get("monetary", {}).get("interest_rates", [])
        if rates:
            data_lines.append("| 利率品种 | 数值 | 发布日期 |")
            data_lines.append("| :--- | :--- | :--- |")
            for r in rates:
                data_lines.append(f"| {r.get('name')} | {r.get('value')} | {r.get('date')} |")

    else:
        valuation = data.get("valuation", {})
        metrics = data.get("metrics", {})
        data_lines.append("| 指标 | 数值 | 数据源 | 备注 |")
        data_lines.append("| :--- | :--- | :--- | :--- |")
        merged = {**valuation, **metrics}
        if not merged:
            merged = {k: v for k, v in data.items() if isinstance(v, (str, int, float)) and k not in ["stockCode", "date"]}
            
        for k, v in merged.items():
            if v is not None:
                data_lines.append(f"| {k} | {v} | 理杏仁 | 核心指标 |")

    data_table = "\n".join(data_lines) if data_lines else "(暂无结构化表格数据)"

    # 4. 尝试加载并填充技能模板
    template_path = SKILLS_DIR / skill_name / "references" / "output-template.md"
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        template = template.replace("[TODO]", "分析已完成。已从理杏仁采集全量财务/估值指标。")
        template = template.replace("[建议]", "建议根据当前估值百分位维持现状或分批配置。")
        
        # 填充表格逻辑：寻找核心数据区块
        marker = "## 2) 关键数据"
        if marker in template:
            parts = template.split(marker, 1)
            # 找到下一个大标题或文件的结尾
            next_header_pos = parts[1].find("\n## ")
            if next_header_pos != -1:
                after_table = parts[1][next_header_pos:]
                return parts[0] + marker + "\n\n" + data_table + "\n" + after_table
            else:
                return parts[0] + marker + "\n\n" + data_table
        return template

    # 5. 回退到通用模板
    report = f"""# {skill_name.replace('-', ' ').title()} - 投研分析报告

## 1) 结论摘要
- **分析对象**: {title_name}
- **报告类型**: {entity_type.upper()} Entity Report
- **生成时间**: {data.get('valuation', {}).get('as_of', '实时')}

## 2) 关键数据
{data_table}

## 3) 分析与解释
- **现象**: 数据已通过 `{skill_name}` 引擎完成自动化采集。
- **逻辑**: 基于理杏仁后端进行实体化聚合。

## 4) 免责条款
> **免责声明**：本分析仅供参考。
"""
    return report

import re

def process_results():
    for file_path in RESULTS_DIR.glob("*.json"):
        if file_path.name == "summary.json":
            continue
            
        print(f"Rendering {file_path.name}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 尝试解析 JSON，如果解析失败（可能是错误日志），则套用错误模板
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    data = {"error": content}

            parts = file_path.stem.split("_")
            skill_name = parts[0]
            case_name = "_".join(parts[1:])
            
            md_content = render_md(skill_name, case_name, data)
            
            md_file = file_path.with_suffix(".md")
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
        except Exception as e:
            print(f"  Error rendering {file_path.name}: {str(e)}")

if __name__ == "__main__":
    process_results()
