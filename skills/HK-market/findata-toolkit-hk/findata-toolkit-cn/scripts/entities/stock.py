from common.lixinger_client import LixingerClient
from datetime import datetime

class StockEntity:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()

    def get_full_report(self, stock_code: str, mode: str = "brief") -> dict:
        """
        获取个股全能报告。
        mode: brief (摘要) / full (详尽)
        """
        # 1. 基础信息
        basic = self.client.fetch("hk/company", {"stockCodes": [stock_code]})
        if not basic or not basic.get('data'):
            return {"error": f"Stock {stock_code} not found."}
        
        info = basic['data'][0]
        
        # 2. 核心指标与估值 (PE/PB/市值)
        # 很多接口需要显式提供 date 或 startDate
        today_str = datetime.now().strftime("%Y-%m-%d")
        metrics_res = self.client.fetch("hk/company/fundamental/non_financial", {
            "stockCodes": [stock_code],
            "metricsList": ["pe_ttm", "pb", "mc"],
            "date": today_str,
            "limit": 1
        })
        if not metrics_res or metrics_res.get('code') != 1 or not metrics_res.get('data'):
             # Fallback: 使用 startDate 获取最近的一条数据
             metrics_res = self.client.fetch("hk/company/fundamental/non_financial", {
                "stockCodes": [stock_code],
                "metricsList": ["pe_ttm", "pb", "mc"],
                "startDate": "2024-01-01",
                "limit": 1
            })
        
        # Lixinger 的 data 可能是个列表（即使 limit=1），按日期倒序排我们需要最后一个或者第一个
        # 通常 startDate + limit=1 返回的是第一条（即最老的那条），所以我们需要用 endDate + limit=1 吗？
        # 实际上 Lixinger API 默认是按日期倒序的。
        metrics = metrics_res['data'][0] if metrics_res and metrics_res.get('data') else {}

        # 3. 构造结果
        report = {
            "identity": {
                "name": info.get("name"),
                "code": info.get("stockCode"),
                "market": info.get("market"),
                "ipoDate": info.get("ipoDate")
            },
            "valuation": {
                "pe_ttm": metrics.get("pe_ttm"),
                "pb": metrics.get("pb"),
                "market_cap_billion": metrics.get("mc"), # mc 已经通过 client 的转换变为了亿元（如果有配置的话）
                "as_of": metrics.get("date")
            },
            "metrics": {
                "note": "Detailed financial metrics (ROE/Revenue) require specific metricsList in cn/company/financial-statement"
            }
        }

        # 4. 如果是 Full 模式，增加历史 K 线或更多字段
        if mode == "full":
            # 增加最近 5 天行情
            # 注意：cn/company/candlestick 需要 type, startDate, endDate
            today_str = datetime.now().strftime("%Y-%m-%d")
            kline_res = self.client.fetch("hk/company/candlestick", {
                "stockCode": stock_code,
                "type": "ex_rights",
                "startDate": "2026-01-01", 
                "endDate": today_str,
                "limit": 5,
                "period": "daily"
            })
            report["recent_kline"] = kline_res.get('data', [])
            
            # 增加高管变动
            executive_res = self.client.fetch("hk/company/executive-shareholding", {
                "stockCodes": [stock_code],
                "limit": 5
            })
            report["recent_executive_trades"] = executive_res.get('data', [])

        return report

def get_stock_entity(code: str, mode: str = "brief"):
    return StockEntity().get_full_report(code, mode)
