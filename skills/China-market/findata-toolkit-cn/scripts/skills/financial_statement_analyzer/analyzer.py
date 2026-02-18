from common.lixinger_client import LixingerClient
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class FinancialStatementAnalyzer:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()
        self.current_year = datetime.now().year

    def get_financial_statements(self, stock_code: str, years: int = 5) -> Dict:
        """
        获取三大报表(资产负债表/利润表/现金流量表)最近N年数据
        """
        end_date = f"{self.current_year}-12-31"
        start_date = f"{self.current_year - years}-01-01"

        # 利润表指标
        income_metrics = [
            "revenue", "operating_revenue", "net_profit", "net_profit_after_deduction",
            "gross_profit_margin", "net_profit_margin", "operating_profit",
            "operating_expense", "sales_expense", "management_expense", "finance_expense",
            "income_tax_expense", "basic_eps", "diluted_eps"
        ]

        # 资产负债表指标
        balance_metrics = [
            "total_assets", "current_assets", "non_current_assets",
            "total_liabilities", "current_liabilities", "non_current_liabilities",
            "total_equity", "monetary_funds", "accounts_receivable", "inventory",
            "fixed_assets", "intangible_assets", "goodwill", "short_term_loan",
            "long_term_loan", "accounts_payable", "retained_earnings", "capital_reserve"
        ]

        # 现金流量表指标
        cashflow_metrics = [
            "operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
            "cash_and_cash_equivalents_increase", "end_balance_of_cash_and_cash_equivalents",
            "sales_of_goods_and_provision_of_services_received_cash",
            "payment_to_employees_and_for_employees_cash",
            "payment_of_all_types_of_taxes_cash"
        ]

        all_metrics = list(set(income_metrics + balance_metrics + cashflow_metrics))

        # 获取年报财务数据
        params = {
            "stockCodes": [stock_code],
            "metricsList": all_metrics,
            "startDate": start_date,
            "endDate": end_date,
            "limit": years * 2,
            "reportType": "annual"
        }

        result = self.client.fetch("cn/company/financial-statement", params)

        if not result or result.get('code') != 1 or not result.get('data'):
            return {"error": f"Failed to fetch financial statements for {stock_code}"}

        data = result['data']
        # 按年份排序
        data.sort(key=lambda x: x['date'], reverse=True)

        statements = {
            "income_statement": [],
            "balance_sheet": [],
            "cashflow_statement": []
        }

        for item in data:
            year = item['date'].split('-')[0]
            # 利润表
            income_item = {"year": year, "date": item['date']}
            for metric in income_metrics:
                income_item[metric] = item.get(metric)
            statements["income_statement"].append(income_item)

            # 资产负债表
            balance_item = {"year": year, "date": item['date']}
            for metric in balance_metrics:
                balance_item[metric] = item.get(metric)
            statements["balance_sheet"].append(balance_item)

            # 现金流量表
            cashflow_item = {"year": year, "date": item['date']}
            for metric in cashflow_metrics:
                cashflow_item[metric] = item.get(metric)
            statements["cashflow_statement"].append(cashflow_item)

        return statements

    def calculate_dupont_analysis(self, statements: Dict) -> List[Dict]:
        """
        杜邦分析：ROE = 净利率 × 资产周转率 × 杠杆率
        """
        dupont_data = []

        income = statements.get("income_statement", [])
        balance = statements.get("balance_sheet", [])

        for inc, bal in zip(income, balance):
            year = inc['year']
            net_profit = inc.get('net_profit', 0) or 0
            revenue = inc.get('revenue', 0) or 0
            total_assets = bal.get('total_assets', 0) or 0
            total_equity = bal.get('total_equity', 0) or 0

            net_profit_margin = net_profit / revenue * 100 if revenue > 0 else 0
            asset_turnover = revenue / total_assets if total_assets > 0 else 0
            leverage_ratio = total_assets / total_equity if total_equity > 0 else 0
            roe = net_profit_margin * asset_turnover * leverage_ratio

            dupont_data.append({
                "year": year,
                "roe": round(roe, 2),
                "net_profit_margin": round(net_profit_margin, 2),
                "asset_turnover": round(asset_turnover, 4),
                "leverage_ratio": round(leverage_ratio, 2),
                "net_profit": net_profit,
                "revenue": revenue,
                "total_assets": total_assets,
                "total_equity": total_equity
            })

        return dupont_data

    def analyze_cashflow_quality(self, statements: Dict) -> List[Dict]:
        """
        现金流质量分析：经营现金流与净利润匹配度
        """
        quality_data = []

        income = statements.get("income_statement", [])
        cashflow = statements.get("cashflow_statement", [])

        for inc, cf in zip(income, cashflow):
            year = inc['year']
            net_profit = inc.get('net_profit', 0) or 0
            operating_cf = cf.get('operating_cash_flow', 0) or 0
            revenue = inc.get('revenue', 0) or 0
            sales_cash = cf.get('sales_of_goods_and_provision_of_services_received_cash', 0) or 0

            cf_profit_ratio = operating_cf / net_profit * 100 if net_profit != 0 else 0
            sales_cash_ratio = sales_cash / revenue * 100 if revenue > 0 else 0

            quality_assessment = "优秀" if cf_profit_ratio >= 100 else \
                                "良好" if cf_profit_ratio >= 80 else \
                                "一般" if cf_profit_ratio >= 50 else \
                                "较差"

            quality_data.append({
                "year": year,
                "net_profit": net_profit,
                "operating_cash_flow": operating_cf,
                "cash_to_profit_ratio": round(cf_profit_ratio, 2),
                "sales_cash_received_ratio": round(sales_cash_ratio, 2),
                "quality_assessment": quality_assessment
            })

        return quality_data

    def identify_fraud_risks(self, statements: Dict) -> Dict:
        """
        财务造假风险识别：存贷双高/商誉减值/大股东占款等预警
        """
        risks = []
        latest_balance = statements.get("balance_sheet", [])[0] if statements.get("balance_sheet") else {}
        latest_year = latest_balance.get('year', 'N/A')

        # 存贷双高风险
        monetary_funds = latest_balance.get('monetary_funds', 0) or 0
        short_term_loan = latest_balance.get('short_term_loan', 0) or 0
        long_term_loan = latest_balance.get('long_term_loan', 0) or 0
        total_interest_bearing_debt = short_term_loan + long_term_loan

        if monetary_funds > 0 and total_interest_bearing_debt > monetary_funds * 0.8:
            risks.append({
                "risk_type": "存贷双高风险",
                "level": "高",
                "description": f"货币资金({monetary_funds}亿)远低于有息负债({total_interest_bearing_debt}亿)，存在大存大贷异常",
                "year": latest_year
            })

        # 商誉减值风险
        goodwill = latest_balance.get('goodwill', 0) or 0
        net_assets = latest_balance.get('total_equity', 0) or 0

        if goodwill > 0 and net_assets > 0 and goodwill / net_assets > 0.3:
            risks.append({
                "risk_type": "商誉减值风险",
                "level": "中" if goodwill/net_assets < 0.5 else "高",
                "description": f"商誉占净资产比例达{round(goodwill/net_assets*100, 2)}%，存在减值风险",
                "year": latest_year
            })

        # 应收账款风险
        accounts_receivable = latest_balance.get('accounts_receivable', 0) or 0
        revenue = statements.get('income_statement', [])[0].get('revenue', 0) if statements.get('income_statement') else 0

        if accounts_receivable > 0 and revenue > 0 and accounts_receivable / revenue > 0.5:
            risks.append({
                "risk_type": "应收账款风险",
                "level": "中" if accounts_receivable/revenue < 0.7 else "高",
                "description": f"应收账款占营业收入比例达{round(accounts_receivable/revenue*100, 2)}%，回款能力弱",
                "year": latest_year
            })

        # 存货风险
        inventory = latest_balance.get('inventory', 0) or 0
        current_assets = latest_balance.get('current_assets', 0) or 0

        if inventory > 0 and current_assets > 0 and inventory / current_assets > 0.5:
            risks.append({
                "risk_type": "存货积压风险",
                "level": "中" if inventory/current_assets < 0.7 else "高",
                "description": f"存货占流动资产比例达{round(inventory/current_assets*100, 2)}%，存在积压减值风险",
                "year": latest_year
            })

        return {
            "total_risks": len(risks),
            "risk_level": "高" if any(r['level'] == '高' for r in risks) else "中" if len(risks) >=2 else "低",
            "risk_details": risks
        }

    def analyze_operation_efficiency(self, statements: Dict) -> List[Dict]:
        """
        运营效率分析
        """
        efficiency_data = []

        income = statements.get("income_statement", [])
        balance = statements.get("balance_sheet", [])

        for i in range(len(income)):
            inc = income[i]
            bal = balance[i]
            year = inc['year']

            revenue = inc.get('revenue', 0) or 0
            operating_cost = inc.get('operating_revenue', 0) or 0  # 近似营业成本
            accounts_receivable = bal.get('accounts_receivable', 0) or 0
            inventory = bal.get('inventory', 0) or 0
            total_assets = bal.get('total_assets', 0) or 0

            # 应收账款周转率
            ar_turnover = revenue / accounts_receivable * 365 if accounts_receivable > 0 else 0
            # 存货周转率
            inventory_turnover = operating_cost / inventory * 365 if inventory > 0 else 0
            # 总资产周转率
            asset_turnover = revenue / total_assets if total_assets > 0 else 0

            efficiency_data.append({
                "year": year,
                "accounts_receivable_days": round(ar_turnover, 1),
                "inventory_days": round(inventory_turnover, 1),
                "total_asset_turnover": round(asset_turnover, 4),
                "assessment": "优秀" if asset_turnover > 1 else "良好" if asset_turnover > 0.5 else "一般" if asset_turnover > 0.2 else "较差"
            })

        return efficiency_data

    def analyze_solvency(self, statements: Dict) -> List[Dict]:
        """
        偿债能力分析
        """
        solvency_data = []

        balance = statements.get("balance_sheet", [])

        for bal in balance:
            year = bal['year']
            current_assets = bal.get('current_assets', 0) or 0
            current_liabilities = bal.get('current_liabilities', 0) or 0
            total_assets = bal.get('total_assets', 0) or 0
            total_liabilities = bal.get('total_liabilities', 0) or 0
            monetary_funds = bal.get('monetary_funds', 0) or 0

            # 流动比率
            current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
            # 速动比率
            quick_ratio = (current_assets - bal.get('inventory', 0) or 0) / current_liabilities if current_liabilities > 0 else 0
            # 资产负债率
            debt_to_asset_ratio = total_liabilities / total_assets * 100 if total_assets > 0 else 0
            # 现金比率
            cash_ratio = monetary_funds / current_liabilities if current_liabilities > 0 else 0

            solvency_data.append({
                "year": year,
                "current_ratio": round(current_ratio, 2),
                "quick_ratio": round(quick_ratio, 2),
                "debt_to_asset_ratio": round(debt_to_asset_ratio, 2),
                "cash_ratio": round(cash_ratio, 2),
                "assessment": "优秀" if current_ratio > 2 and debt_to_asset_ratio < 50 else \
                             "良好" if current_ratio > 1.5 and debt_to_asset_ratio < 60 else \
                             "一般" if current_ratio > 1 and debt_to_asset_ratio < 70 else \
                             "较差"
            })

        return solvency_data

    def analyze_growth(self, statements: Dict) -> List[Dict]:
        """
        成长能力分析
        """
        growth_data = []
        income = statements.get("income_statement", [])
        balance = statements.get("balance_sheet", [])

        for i in range(len(income)-1):
            current_year = income[i]['year']
            current_revenue = income[i].get('revenue', 0) or 0
            current_net_profit = income[i].get('net_profit', 0) or 0
            current_total_assets = balance[i].get('total_assets', 0) or 0

            prev_revenue = income[i+1].get('revenue', 0) or 0
            prev_net_profit = income[i+1].get('net_profit', 0) or 0
            prev_total_assets = balance[i+1].get('total_assets', 0) or 0

            revenue_growth = (current_revenue - prev_revenue) / prev_revenue * 100 if prev_revenue > 0 else 0
            profit_growth = (current_net_profit - prev_net_profit) / prev_net_profit * 100 if prev_net_profit != 0 else 0
            asset_growth = (current_total_assets - prev_total_assets) / prev_total_assets * 100 if prev_total_assets > 0 else 0

            growth_data.append({
                "year": current_year,
                "revenue_yoy_growth": round(revenue_growth, 2),
                "net_profit_yoy_growth": round(profit_growth, 2),
                "total_asset_yoy_growth": round(asset_growth, 2),
                "assessment": "高速成长" if profit_growth > 30 else \
                             "稳定成长" if profit_growth > 10 else \
                             "增长乏力" if profit_growth > 0 else \
                             "衰退"
            })

        return growth_data

    def get_full_analysis(self, stock_code: str, years: int = 5) -> Dict:
        """
        获取完整的财报深度分析报告
        """
        # 1. 获取三大报表
        statements = self.get_financial_statements(stock_code, years)
        if "error" in statements:
            return statements

        # 2. 杜邦分析
        dupont = self.calculate_dupont_analysis(statements)

        # 3. 现金流质量分析
        cashflow_quality = self.analyze_cashflow_quality(statements)

        # 4. 财务风险识别
        fraud_risks = self.identify_fraud_risks(statements)

        # 5. 运营效率分析
        operation_efficiency = self.analyze_operation_efficiency(statements)

        # 6. 偿债能力分析
        solvency = self.analyze_solvency(statements)

        # 7. 成长能力分析
        growth = self.analyze_growth(statements)

        # 8. 综合评分
        latest_roe = dupont[0]['roe'] if dupont else 0
        latest_cf_ratio = cashflow_quality[0]['cash_to_profit_ratio'] if cashflow_quality else 0
        latest_debt_ratio = solvency[0]['debt_to_asset_ratio'] if solvency else 0
        latest_profit_growth = growth[0]['net_profit_yoy_growth'] if growth else 0

        score = 0
        score += min(latest_roe * 2, 30)  # ROE 最高30分
        score += min(latest_cf_ratio * 0.2, 25)  # 现金流占比 最高25分
        score += max(0, 25 - latest_debt_ratio * 0.3)  # 负债率越低分越高 最高25分
        score += min(max(latest_profit_growth, 0) * 0.4, 20)  # 利润增长 最高20分

        overall_rating = "A+" if score >= 85 else \
                        "A" if score >= 75 else \
                        "B+" if score >= 65 else \
                        "B" if score >= 55 else \
                        "C" if score >= 45 else \
                        "D"

        return {
            "stock_code": stock_code,
            "analysis_as_of": datetime.now().strftime("%Y-%m-%d"),
            "time_range": f"最近{years}年",
            "financial_statements": statements,
            "dupont_analysis": dupont,
            "cashflow_quality_analysis": cashflow_quality,
            "fraud_risk_identification": fraud_risks,
            "operation_efficiency_analysis": operation_efficiency,
            "solvency_analysis": solvency,
            "growth_analysis": growth,
            "comprehensive_score": round(score, 1),
            "overall_rating": overall_rating
        }

def run_analysis(stock_code: str, years: int = 5) -> Dict:
    """
    外部调用入口
    """
    analyzer = FinancialStatementAnalyzer()
    return analyzer.get_full_analysis(stock_code, years)
