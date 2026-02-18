from common.lixinger_client import LixingerClient

class SectorEntity:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()

    def get_sector_detail(self, sector_code: str) -> dict:
        """
        获取行业/板块详情。
        """
        detail = {}

        # 1. 行业基本信息
        basic = self.client.fetch("us/industry", {"stockCodes": [sector_code]})
        detail["identity"] = basic.get('data', [{}])[0]

        # 2. 行业估值 (PE/PB)
        valuation = self.client.fetch("us/industry/valuation", {
            "stockCodes": [sector_code],
            "limit": 1
        })
        detail["valuation"] = valuation.get('data', [{}])[0]

        # 3. 行业成分股 (Top N)
        constituents = self.client.fetch("us/industry/constituents", {
            "stockCode": sector_code
        })
        detail["constituents_summary"] = {
            "count": len(constituents.get('data', [])),
            "sample": constituents.get('data', [])[:10]
        }

        return detail

def get_sector_entity(code: str):
    return SectorEntity().get_sector_detail(code)
