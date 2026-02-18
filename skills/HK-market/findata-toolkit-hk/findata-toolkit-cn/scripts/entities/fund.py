from common.lixinger_client import LixingerClient

class FundEntity:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()

    def get_fund_report(self, fund_code: str) -> dict:
        """
        获取基金全能报告。
        """
        report = {}

        # 1. 基金基础信息
        basic = self.client.fetch("hk/fund", {"stockCodes": [fund_code]})
        report["identity"] = basic.get('data', [{}])[0]

        # 2. 最新净值
        nav = self.client.fetch("hk/fund/net-value", {
            "stockCodes": [fund_code],
            "limit": 1
        })
        report["latest_nav"] = nav.get('data', [{}])[0]

        # 3. 基金持仓 (Top 10)
        holdings = self.client.fetch("hk/fund/holdings", {
            "stockCode": fund_code
        })
        report["top_holdings"] = holdings.get('data', [])[:10]

        # 4. 基金评级
        rating = self.client.fetch("hk/fund/rating", {
            "stockCodes": [fund_code]
        })
        report["ratings"] = rating.get('data', [])

        return report

def get_fund_entity(code: str):
    return FundEntity().get_fund_report(code)
