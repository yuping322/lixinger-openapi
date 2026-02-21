"""示例客户端"""

import requests
from typing import Dict, Any, Optional


class FindataClient:
    """Findata Service 客户端"""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET 请求"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST 请求"""
        return self._request("POST", endpoint, json=data)

    # ============ 股票接口 ============

    def get_stock_basic(self, symbol: str) -> Dict[str, Any]:
        """获取股票基础信息"""
        return self.get(f"/api/cn/stock/{symbol}/basic")

    def get_stock_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "ex_rights"
    ) -> Dict[str, Any]:
        """获取股票历史行情"""
        return self.get(
            f"/api/cn/stock/{symbol}/history",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "period": period,
                "adjust": adjust
            }
        )

    def get_stock_realtime(self, symbol: str) -> Dict[str, Any]:
        """获取股票实时行情"""
        return self.get(f"/api/cn/stock/{symbol}/realtime")

    def get_stock_financial(
        self,
        symbol: str,
        statement_type: str = "balance_sheet",
        limit: int = 5
    ) -> Dict[str, Any]:
        """获取股票财务数据"""
        return self.get(
            f"/api/cn/stock/{symbol}/financial",
            params={"statement_type": statement_type, "limit": limit}
        )

    def get_stock_valuation(self, symbol: str) -> Dict[str, Any]:
        """获取股票估值指标"""
        return self.get(f"/api/cn/stock/{symbol}/valuation")

    # ============ 市场接口 ============

    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概览"""
        return self.get("/api/cn/market/overview")

    # ============ 宏观接口 ============

    def get_macro_lpr(self) -> Dict[str, Any]:
        """获取LPR利率"""
        return self.get("/api/cn/macro/lpr")

    def get_macro_cpi(self) -> Dict[str, Any]:
        """获取CPI数据"""
        return self.get("/api/cn/macro/cpi")

    def get_macro_ppi(self) -> Dict[str, Any]:
        """获取PPI数据"""
        return self.get("/api/cn/macro/ppi")

    def get_macro_pmi(self) -> Dict[str, Any]:
        """获取PMI数据"""
        return self.get("/api/cn/macro/pmi")

    def get_macro_m2(self) -> Dict[str, Any]:
        """获取M2货币供应"""
        return self.get("/api/cn/macro/m2")

    # ============ 资金流向接口 ============

    def get_fund_flow_stock(self, symbol: str) -> Dict[str, Any]:
        """获取个股资金流向"""
        return self.get(f"/api/cn/flow/stock/{symbol}")

    def get_fund_flow_index(self, index_code: str) -> Dict[str, Any]:
        """获取指数资金流向"""
        return self.get(f"/api/cn/flow/index/{index_code}")

    def get_fund_flow_industry(self, industry_code: str = None) -> Dict[str, Any]:
        """获取行业资金流向"""
        params = {"industry_code": industry_code} if industry_code else {}
        return self.get("/api/cn/flow/industry", params=params)

    # ============ 行业板块接口 ============

    def get_industry_list(self) -> Dict[str, Any]:
        """获取行业列表"""
        return self.get("/api/cn/board/industry/list")

    def get_industry_kline(self, industry_code: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取行业K线"""
        return self.get(
            f"/api/cn/board/industry/{industry_code}/kline",
            params={"start_date": start_date, "end_date": end_date}
        )

    def get_industry_stocks(self, industry_code: str) -> Dict[str, Any]:
        """获取行业成分股"""
        return self.get(f"/api/cn/board/industry/{industry_code}/stocks")

    def get_industry_valuation(self, industry_code: str) -> Dict[str, Any]:
        """获取行业估值"""
        return self.get(f"/api/cn/board/industry/{industry_code}/valuation")

    def get_index_list(self) -> Dict[str, Any]:
        """获取指数列表"""
        return self.get("/api/cn/board/index/list")

    def get_index_kline(self, index_code: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取指数K线"""
        return self.get(
            f"/api/cn/board/index/{index_code}/kline",
            params={"start_date": start_date, "end_date": end_date}
        )

    def get_index_constituents(self, index_code: str) -> Dict[str, Any]:
        """获取指数成分股"""
        return self.get(f"/api/cn/board/index/{index_code}/constituents")

    # ============ 特殊数据接口 ============

    def get_dragon_tiger(self, symbol: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """获取龙虎榜数据"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self.get(f"/api/cn/special/dragon-tiger/{symbol}", params=params)

    def get_block_deal(self, symbol: str) -> Dict[str, Any]:
        """获取大宗交易数据"""
        return self.get(f"/api/cn/special/block-deal/{symbol}")

    def get_equity_pledge(self, symbol: str) -> Dict[str, Any]:
        """获取股权质押数据"""
        return self.get(f"/api/cn/special/equity-pledge/{symbol}")

    # ============ 股东信息接口 ============

    def get_shareholders(self, symbol: str) -> Dict[str, Any]:
        """获取股东信息"""
        return self.get(f"/api/cn/shareholder/{symbol}")

    def get_shareholders_count(self, symbol: str) -> Dict[str, Any]:
        """获取股东人数"""
        return self.get(f"/api/cn/shareholder/{symbol}/count")

    def get_executive_shareholding(self, symbol: str) -> Dict[str, Any]:
        """获取高管增减持"""
        return self.get(f"/api/cn/shareholder/{symbol}/executive")

    def get_major_shareholder_change(self, symbol: str) -> Dict[str, Any]:
        """获取大股东增减持"""
        return self.get(f"/api/cn/shareholder/{symbol}/major")

    # ============ 分红配股接口 ============

    def get_dividend(self, symbol: str) -> Dict[str, Any]:
        """获取分红送配数据"""
        return self.get(f"/api/cn/dividend/{symbol}")


# 使用示例
if __name__ == "__main__":
    # 初始化客户端
    client = FindataClient(base_url="http://localhost:8000")

    # 测试股票基础信息
    print("=" * 80)
    print("测试股票基础信息:")
    result = client.get_stock_basic("600519")  # 贵州茅台
    print(f"响应: code={result['code']}, count={result['meta']['count']}")
    if result['data']:
        print(f"股票名称: {result['data'][0].get('name')}")

    # 测试历史行情
    print("\n" + "=" * 80)
    print("测试股票历史行情:")
    result = client.get_stock_history("600519", "2024-01-01", "2024-01-31")
    print(f"响应: code={result['code']}, count={result['meta']['count']}")
    if result['data']:
        print(f"第一条数据: {result['data'][0]}")

    # 测试实时行情
    print("\n" + "=" * 80)
    print("测试股票实时行情:")
    result = client.get_stock_realtime("600519")
    print(f"响应: code={result['code']}, count={result['meta']['count']}")
    if result['data']:
        print(f"最新价: {result['data'][0].get('close')}")

    # 测试市场概览
    print("\n" + "=" * 80)
    print("测试市场概览:")
    result = client.get_market_overview()
    print(f"响应: code={result['code']}, count={result['meta']['count']}")
    if result['data']:
        print(f"指数数量: {len(result['data'])}")

    # 测试宏观数据
    print("\n" + "=" * 80)
    print("测试LPR数据:")
    result = client.get_macro_lpr()
    print(f"响应: code={result['code']}, count={result['meta']['count']}")
    if result['data']:
        print(f"最新LPR: {result['data'][0]}")

    print("\n" + "=" * 80)
    print("所有测试完成!")
