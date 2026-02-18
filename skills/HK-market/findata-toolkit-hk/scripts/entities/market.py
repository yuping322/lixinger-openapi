from common.lixinger_client import LixingerClient
from common.utils import safe_change_pct

class MarketEntity:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()

    def get_market_overview(self) -> dict:
        """
        获取全市场概况（指数表现、核心估值）。
        """
        overview = {}

        # 1. 核心指数表现 (SSE 50, HS 300, CSI 500, SZSE Component)
        # 港股指数
        indices = ["HSI", "HSCEI", "HSCCI"]
        major_indices = []
        last_date = ""

        for code in indices:
            res = self.client.fetch("hk/index/candlestick", {
                "stockCode": code,
                "type": "normal",
                "limit": 1,
                "period": "daily"
            })
            
            if res and res.get('data'):
                item = res['data'][0]
                major_indices.append({
                    "name": code, # Use code as name (candlestick index doesn't return stockCode in data)
                    "latest": item.get('close'),
                    "change_pct": round(safe_change_pct(item.get('close'), item.get('open'), default=0) * 100, 2),
                    "date": item.get('date')
                })
                if not last_date:
                    last_date = item.get('date')
        
        overview["major_indices"] = major_indices

        # 2. 市场估值水位 (以沪深 300 为代表)
        if last_date:
            valuation_res = self.client.fetch("hk/index/fundamental", {
                "stockCodes": ["000300"],
                "date": last_date,
                "metricsList": ["pe_ttm.mcw", "pb.mcw"]
            })
            if valuation_res and valuation_res.get('data'):
                overview["valuation_overview"] = valuation_res['data'][0]

        # 3. 占位：市场情绪
        overview["sentiment"] = {
            "description": "市场整体成交额及涨跌分位数处理中...",
            "note": "Sentiment data requires daily summary aggregation."
        }

        return overview

def get_market_entity():
    return MarketEntity().get_market_overview()
