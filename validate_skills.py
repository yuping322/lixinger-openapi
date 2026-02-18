#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金融技能逻辑合理性验证脚本
验证范围：A股、港股、美股各56个技能
验证维度：
1. 返回字段符合金融行业标准
2. 计算逻辑正确性
3. 业务逻辑符合投资分析需求
4. 识别不符合常识的输出
"""

import json
import os
import re
from typing import Dict, List, Tuple, Any

# 金融字段标准定义
FINANCIAL_FIELD_STANDARDS = {
    # 估值类
    "pe": {"type": "number", "min": 0, "max": 1000, "description": "市盈率，不能为负，合理范围0-1000"},
    "pe_ttm": {"type": "number", "min": 0, "max": 1000, "description": "动态市盈率，不能为负，合理范围0-1000"},
    "pb": {"type": "number", "min": 0, "max": 100, "description": "市净率，不能为负，合理范围0-100"},
    "ps": {"type": "number", "min": 0, "max": 100, "description": "市销率，不能为负，合理范围0-100"},
    "ps_ttm": {"type": "number", "min": 0, "max": 100, "description": "动态市销率，不能为负，合理范围0-100"},
    "pcf": {"type": "number", "min": -1000, "max": 1000, "description": "市现率，合理范围-1000到1000"},
    "dividend_yield": {"type": "number", "min": 0, "max": 50, "description": "股息率，百分比，合理范围0-50%"},

    # 财务类
    "market_cap": {"type": "number", "min": 1000000, "max": 1e15, "description": "市值，单位元，最小100万，最大1e15"},
    "circulating_market_cap": {"type": "number", "min": 0, "max": 1e15, "description": "流通市值，单位元，合理范围0到1e15"},
    "total_shares": {"type": "number", "min": 1, "max": 1e12, "description": "总股本，合理范围1到1e12"},
    "circulating_shares": {"type": "number", "min": 0, "max": 1e12, "description": "流通股本，合理范围0到1e12"},

    # 行情类
    "close": {"type": "number", "min": 0.01, "max": 1000000, "description": "收盘价，最小0.01元"},
    "open": {"type": "number", "min": 0.01, "max": 1000000, "description": "开盘价，最小0.01元"},
    "high": {"type": "number", "min": 0.01, "max": 1000000, "description": "最高价，最小0.01元"},
    "low": {"type": "number", "min": 0.01, "max": 1000000, "description": "最低价，最小0.01元"},
    "volume": {"type": "number", "min": 0, "max": 1e12, "description": "成交量，合理范围0到1e12"},
    "turnover": {"type": "number", "min": 0, "max": 1e12, "description": "成交额，合理范围0到1e12"},
    "change_percent": {"type": "number", "min": -50, "max": 50, "description": "涨跌幅，百分比，合理范围-50%到50%"},
    "turnover_rate": {"type": "number", "min": 0, "max": 100, "description": "换手率，百分比，合理范围0到100%"},

    # 财务指标类
    "roe": {"type": "number", "min": -100, "max": 100, "description": "净资产收益率，百分比，合理范围-100%到100%"},
    "roa": {"type": "number", "min": -100, "max": 100, "description": "总资产收益率，百分比，合理范围-100%到100%"},
    "gross_margin": {"type": "number", "min": -100, "max": 100, "description": "毛利率，百分比，合理范围-100%到100%"},
    "net_margin": {"type": "number", "min": -100, "max": 100, "description": "净利率，百分比，合理范围-100%到100%"},
    "debt_to_assets": {"type": "number", "min": 0, "max": 100, "description": "资产负债率，百分比，合理范围0到100%"},
    "current_ratio": {"type": "number", "min": 0, "max": 100, "description": "流动比率，合理范围0到100"},
    "quick_ratio": {"type": "number", "min": 0, "max": 100, "description": "速动比率，合理范围0到100"},

    # 增长类
    "revenue_growth_rate": {"type": "number", "min": -100, "max": 1000, "description": "营收增长率，百分比，合理范围-100%到1000%"},
    "net_profit_growth_rate": {"type": "number", "min": -100, "max": 1000, "description": "净利润增长率，百分比，合理范围-100%到1000%"},
    "eps_growth_rate": {"type": "number", "min": -100, "max": 1000, "description": "EPS增长率，百分比，合理范围-100%到1000%"},
}

# 市场特殊规则
MARKET_SPECIAL_RULES = {
    "cn": {
        "stock_price_limit": 10,  # 普通股票涨跌幅限制10%
        "st_price_limit": 5,      # ST股票涨跌幅限制5%
        "new_stock_price_limit": 44,  # 新股首日涨跌幅限制44%
    },
    "hk": {
        "price_limit": None,  # 港股无涨跌幅限制
    },
    "us": {
        "price_limit": None,  # 美股无涨跌幅限制
    }
}

class SkillValidator:
    def __init__(self, market: str, skill_dir: str):
        self.market = market
        self.skill_dir = skill_dir
        self.validation_results = []
        self.total_skills = 0
        self.passed_skills = 0
        self.failed_skills = 0

    def load_skill_definitions(self) -> List[Dict]:
        """加载技能定义文件"""
        litellm_tools_path = os.path.join(self.skill_dir, "config/litellm_tools.json")
        if not os.path.exists(litellm_tools_path):
            raise FileNotFoundError(f"技能配置文件不存在: {litellm_tools_path}")

        with open(litellm_tools_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_skill(self, skill: Dict) -> Tuple[bool, List[str]]:
        """验证单个技能"""
        issues = []
        # 适配实际的技能结构：数据在function字段下
        function_def = skill.get("function", {})
        skill_name = function_def.get("name", "未知技能")
        skill_description = function_def.get("description", "")

        # 1. 基本信息验证
        if not skill_name:
            issues.append("技能名称不能为空")
        if not skill_description:
            issues.append("技能描述不能为空")

        # 2. 参数验证
        parameters = function_def.get("parameters", {})
        properties = parameters.get("properties", {})
        required = parameters.get("required", [])

        # 3. 返回字段验证
        # 检查是否有返回字段定义
        extra = skill.get("extra", {})
        return_fields = extra.get("output", {})
        if not return_fields:
            issues.append("缺少返回字段定义")
        else:
            for field_name, field_def in return_fields.items():
                # 检查字段是否符合金融标准
                normalized_field = field_name.lower().replace(" ", "_")
                if normalized_field in FINANCIAL_FIELD_STANDARDS:
                    standard = FINANCIAL_FIELD_STANDARDS[normalized_field]
                    if field_def.get("type") != standard["type"]:
                        issues.append(f"返回字段{field_name}类型错误，应为{standard['type']}，实际为{field_def.get('type')}")

            # 检查示例数据合理性
            examples = extra.get("examples", {})
            example_data = examples.get("data", "")
            if example_data and "平均市盈率" in example_data:
                # 提取市盈率示例值
                pe_match = re.search(r"平均市盈率\s+(\d+\.?\d*)", example_data)
                if pe_match:
                    pe_value = float(pe_match.group(1))
                    if pe_value < 0 or pe_value > 1000:
                        issues.append(f"示例数据中市盈率{pe_value}超出合理范围(0-1000)")

            # 检查总市值示例
            if "总市值" in example_data:
                cap_match = re.search(r"总市值\s+(\d+\.?\d*)", example_data)
                if cap_match:
                    cap_value = float(cap_match.group(1))
                    if cap_value < 1:  # 单位应该是亿元，所以最小1亿元
                        issues.append(f"示例数据中总市值{cap_value}不合理，不能小于0")

        # 4. 业务逻辑验证
        # 检查技能名称是否符合市场分类
        market_prefixes = {
            "cn": ["cn_", "china_", "a股"],
            "hk": ["hk_", "hongkong_", "港股"],
            "us": ["us_", "usa_", "美股"]
        }

        has_correct_prefix = any(skill_name.lower().startswith(prefix) for prefix in market_prefixes[self.market])
        if not has_correct_prefix and not any(prefix in skill_description.lower() for prefix in market_prefixes[self.market]):
            issues.append(f"技能名称/描述未包含正确的市场标识，应为{self.market}市场相关技能")

        # 5. 计算逻辑合理性检查
        # 检查是否包含不合理的计算逻辑
        skill_code_path = os.path.join(self.skill_dir, f"scripts/{skill_name}.py")
        if os.path.exists(skill_code_path):
            with open(skill_code_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

                # 检查PE计算逻辑
                if "pe" in skill_name.lower() or "市盈率" in skill_description:
                    if re.search(r'pe\s*=\s*.*\/\s*net_profit', code_content) and "if net_profit <= 0" not in code_content:
                        issues.append("PE计算逻辑存在缺陷，未处理净利润为负的情况，可能导致负PE")

                # 检查涨跌幅计算
                if "change" in skill_name.lower() or "涨跌幅" in skill_description:
                    if re.search(r'change_percent\s*=\s*\(.*-.*\)\/.*', code_content) and "if close == 0" not in code_content:
                        issues.append("涨跌幅计算逻辑存在缺陷，未处理分母为0的情况")

                # 检查市值计算
                if "market_cap" in skill_name.lower() or "市值" in skill_description:
                    if re.search(r'market_cap\s*=\s*.*\*.*', code_content) and "if price <= 0 or shares <= 0" not in code_content:
                        issues.append("市值计算逻辑存在缺陷，未处理股价或股本为0/负的情况")

        # 6. 市场特殊规则验证
        if self.market == "cn" and "k_line" in skill_name.lower():
            if "change_percent" in return_fields:
                max_change = return_fields["change_percent"].get("maximum", 100)
                if max_change > 44:
                    issues.append(f"A股市场普通股票涨跌幅最大为44%（新股首日），但返回字段设置最大值为{max_change}，不符合规则")

        return len(issues) == 0, issues

    def validate_all_skills(self) -> Dict:
        """验证所有技能"""
        skills = self.load_skill_definitions()
        self.total_skills = len(skills)

        for skill in skills:
            function_def = skill.get("function", {})
            skill_name = function_def.get("name", "未知技能")
            skill_description = function_def.get("description", "")
            passed, issues = self.validate_skill(skill)

            result = {
                "skill_name": skill_name,
                "market": self.market,
                "passed": passed,
                "issues": issues,
                "skill_description": skill_description
            }

            self.validation_results.append(result)

            if passed:
                self.passed_skills += 1
            else:
                self.failed_skills += 1

        return {
            "market": self.market,
            "total_skills": self.total_skills,
            "passed_skills": self.passed_skills,
            "failed_skills": self.failed_skills,
            "pass_rate": round(self.passed_skills / self.total_skills * 100, 2) if self.total_skills > 0 else 0,
            "details": self.validation_results
        }

def generate_validation_report(all_results: List[Dict], output_path: str):
    """生成验证报告"""
    report_content = "# 金融技能逻辑合理性验证报告\n\n"
    report_content += f"生成时间：{os.popen('date +"%Y-%m-%d %H:%M:%S"').read().strip()}\n"
    report_content += "验证范围：A股、港股、美股技能\n\n"

    # 汇总统计
    total_skills = sum(r["total_skills"] for r in all_results)
    total_passed = sum(r["passed_skills"] for r in all_results)
    total_failed = sum(r["failed_skills"] for r in all_results)
    overall_pass_rate = round(total_passed / total_skills * 100, 2) if total_skills > 0 else 0

    report_content += "## 汇总统计\n\n"
    report_content += f"| 市场 | 总技能数 | 通过数 | 失败数 | 通过率 |\n"
    report_content += f"|------|----------|--------|--------|--------|\n"

    for result in all_results:
        report_content += f"| {result['market'].upper()} | {result['total_skills']} | {result['passed_skills']} | {result['failed_skills']} | {result['pass_rate']}% |\n"

    report_content += f"| 合计 | {total_skills} | {total_passed} | {total_failed} | {overall_pass_rate}% |\n\n"

    # 详细问题列表
    report_content += "## 详细问题列表\n\n"

    for result in all_results:
        market = result["market"].upper()
        report_content += f"### {market}市场问题技能\n\n"

        failed_skills = [r for r in result["details"] if not r["passed"]]
        if not failed_skills:
            report_content += "无问题技能\n\n"
            continue

        for skill in failed_skills:
            report_content += f"#### 技能名称：{skill['skill_name']}\n"
            report_content += f"**技能描述**：{skill['skill_description']}\n\n"
            report_content += "**问题列表**：\n"
            for i, issue in enumerate(skill["issues"], 1):
                report_content += f"{i}. {issue}\n"
            report_content += "\n"

    # 问题分类统计
    report_content += "## 问题分类统计\n\n"
    all_issues = []
    for result in all_results:
        for skill in result["details"]:
            all_issues.extend(skill["issues"])

    issue_types = {
        "字段标准不符合": [i for i in all_issues if "类型错误" in i or "范围设置不合理" in i],
        "计算逻辑缺陷": [i for i in all_issues if "计算逻辑存在缺陷" in i],
        "基本信息缺失": [i for i in all_issues if "不能为空" in i or "缺少返回字段定义" in i],
        "市场规则不符合": [i for i in all_issues if "不符合规则" in i or "未包含正确的市场标识" in i],
        "其他": []
    }

    for issue_type, issues in issue_types.items():
        if issues:
            report_content += f"- {issue_type}：{len(issues)}个\n"

    # 改进建议
    report_content += "\n## 改进建议\n\n"
    report_content += "1. **字段标准化**：所有金融字段严格按照行业标准定义类型和合理范围\n"
    report_content += "2. **边界情况处理**：所有计算逻辑增加边界条件检查，避免除零、负值等异常情况\n"
    report_content += "3. **市场规则适配**：不同市场的技能需要严格遵守对应市场的交易规则（如涨跌幅限制等）\n"
    report_content += "4. **完善元数据**：所有技能必须包含明确的名称、描述、参数和返回字段定义\n"
    report_content += "5. **自动化测试**：建议增加单元测试，覆盖正常和异常边界场景\n"

    # 保存报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"验证报告已生成：{output_path}")
    return report_content

def main():
    # 市场配置
    markets = [
        ("cn", "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market/findata-toolkit-cn"),
        ("hk", "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/HK-market/findata-toolkit-hk"),
        ("us", "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/US-market/findata-toolkit-us")
    ]

    all_results = []

    for market, skill_dir in markets:
        print(f"开始验证{market.upper()}市场技能...")
        validator = SkillValidator(market, skill_dir)
        result = validator.validate_all_skills()
        all_results.append(result)
        print(f"{market.upper()}市场验证完成：{result['passed_skills']}/{result['total_skills']} 通过，通过率{result['pass_rate']}%")

    # 生成报告
    output_path = "/Users/fengzhi/Downloads/git/lixinger-openapi/skills_validation_report.md"
    report_content = generate_validation_report(all_results, output_path)

    # 打印简要结果
    print("\n" + "="*50)
    print("验证完成！")
    print(f"总技能数：{sum(r['total_skills'] for r in all_results)}")
    print(f"通过数：{sum(r['passed_skills'] for r in all_results)}")
    print(f"失败数：{sum(r['failed_skills'] for r in all_results)}")
    print(f"总通过率：{round(sum(r['passed_skills'] for r in all_results)/sum(r['total_skills'] for r in all_results)*100, 2)}%")
    print("="*50)

if __name__ == "__main__":
    main()
