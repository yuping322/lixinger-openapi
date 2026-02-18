from common.lixinger_client import LixingerClient

class MacroEntity:
    def __init__(self, client: LixingerClient = None):
        self.client = client or LixingerClient()

    def get_economic_pulse(self) -> dict:
        """
        获取宏观经济脉搏。聚合利率、通胀、货币和景气度数据。
        """
        pulse = {}

        # 1. 利率与货币
        rates = self.client.fetch("macro/interest-rate", {"limit": 1, "startDate": "2024-01-01"})
        money = self.client.fetch("macro/money-supply", {"limit": 1, "startDate": "2024-01-01"})
        pulse["monetary"] = {
            "interest_rates": rates.get('data', []),
            "money_supply_m2": money.get('data', [])
        }

        # 2. 通胀 (CPI/PPI)
        inflation = self.client.fetch("macro/price-index", {"limit": 1, "startDate": "2024-01-01"})
        pulse["inflation"] = inflation.get('data', [])

        # 3. 增长与景气度 (GDP/PMI)
        gdp = self.client.fetch("macro/gdp", {"limit": 1, "startDate": "2024-01-01"})
        pulse["growth"] = gdp.get('data', [])

        return pulse

def get_macro_entity():
    return MacroEntity().get_economic_pulse()
