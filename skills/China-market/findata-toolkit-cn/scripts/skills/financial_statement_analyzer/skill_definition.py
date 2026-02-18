"""
财报深度分析技能
提供三大报表、杜邦分析、现金流质量、财务造假风险识别、多维度财务分析能力
"""

VIEW_NAME = "financial_statement_analyzer"
DESCRIPTION = "上市公司财报深度分析，包含三大报表获取、杜邦分析、现金流质量、财务风险识别、成长/偿债/运营能力分析，支持最近5年历史数据对比"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "stock_code": {
            "type": "string",
            "description": "股票代码，如 600519"
        },
        "years": {
            "type": "integer",
            "description": "分析年份，默认5年",
            "default": 5,
            "minimum": 1,
            "maximum": 10
        }
    },
    "required": ["stock_code"]
}

def plan(params: dict) -> list[dict]:
    """
    计划执行步骤
    """
    return [
        {
            "key": "financial_statement_analyzer",
            "tool": "financial_statement_analyzer",
            "args": params
        }
    ]

def run(params: dict) -> dict:
    """
    执行财报分析
    """
    from .analyzer import FinancialStatementAnalyzer
    analyzer = FinancialStatementAnalyzer()
    stock_code = params.get("stock_code")
    years = params.get("years", 5)
    return analyzer.get_full_analysis(stock_code, years)
