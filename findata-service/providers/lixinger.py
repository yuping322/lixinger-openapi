"""理杏仁数据源提供者"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from cachetools import TTLCache

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token


class LixingerProvider:
    """理杏仁数据源提供者"""

    def __init__(self, token: str):
        self.token = token
        set_token(token, write_token=False)

        # 缓存：实时数据1小时，日线数据24小时
        self.realtime_cache = TTLCache(maxsize=1000, ttl=3600)
        self.daily_cache = TTLCache(maxsize=5000, ttl=86400)
        self.financial_cache = TTLCache(maxsize=2000, ttl=86400 * 7)

    def _fetch(self, endpoint: str, params: dict, cache_type: str = "daily") -> dict:
        """统一的数据获取方法"""
        # 生成缓存键
        cache_key = f"{endpoint}:{str(sorted(params.items()))}"

        # 选择缓存
        cache_map = {
            "realtime": self.realtime_cache,
            "daily": self.daily_cache,
            "financial": self.financial_cache,
        }
        cache = cache_map.get(cache_type, self.daily_cache)

        # 尝试从缓存获取
        if cache_key in cache:
            return cache[cache_key]

        # 调用 API
        result = query_json(endpoint, params)

        # 存入缓存
        if result and result.get("code") == 1:
            cache[cache_key] = result

        return result

    def get_stock_basic(self, symbol: str) -> dict:
        """获取股票基础信息"""
        result = self._fetch("cn/company", {"stockCodes": [symbol]})

        if result and result.get("code") == 1 and result.get("data"):
            return result["data"][0]
        return {}

    def get_stock_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "ex_rights"
    ) -> List[dict]:
        """获取股票历史行情"""
        result = self._fetch(
            "cn/company/candlestick",
            {
                "stockCode": symbol,
                "type": adjust,
                "startDate": start_date,
                "endDate": end_date,
                "period": period,
            },
            cache_type="daily"
        )

        if result and result.get("code") == 1:
            return result.get("data", [])
        return []

    def get_stock_realtime(self, symbol: str) -> dict:
        """获取股票实时行情"""
        from datetime import datetime, timedelta
        # 理杏仁没有专门的实时接口，用最新的日线数据代替
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")  # 扩大到30天
        
        result = self._fetch(
            "cn/company/candlestick",
            {
                "stockCode": symbol,
                "type": "ex_rights",
                "period": "daily",
                "startDate": start_date,
                "endDate": end_date
            },
            cache_type="realtime"
        )

        if result and result.get("code") == 1 and result.get("data"):
            # 返回最新的一条数据
            data_list = result["data"]
            if isinstance(data_list, list) and len(data_list) > 0:
                return data_list[-1]
        return {}

    def get_financial_data(
        self,
        symbol: str,
        statement_type: str,
        limit: int = 5
    ) -> List[dict]:
        """获取财务数据"""
        # 映射财务报表类型
        endpoint_map = {
            "balance_sheet": "cn/company/fundamental/balance",
            "income_statement": "cn/company/fundamental/income",
            "cash_flow": "cn/company/fundamental/cashflow",
        }

        endpoint = endpoint_map.get(statement_type)
        if not endpoint:
            return []

        result = self._fetch(
            endpoint,
            {"stockCodes": [symbol], "limit": limit},
            cache_type="financial"
        )

        if result and result.get("code") == 1:
            return result.get("data", [])
        return []

    def get_market_overview(self) -> List[dict]:
        """获取市场概览"""
        # 获取主要指数的最新行情
        indices = ["000001", "399001", "000300", "000016", "000905"]
        results = []

        for index_code in indices:
            data = self.get_stock_realtime(index_code)
            if data:
                results.append(data)

        return results

    def get_valuation(self, symbol: str, metrics: List[str] = None) -> dict:
        """获取估值指标 - ⚠️ 理杏仁免费版可能不提供此数据"""
        # 理杏仁免费版通常不提供估值数据
        # 返回空字典，由路由层处理友好提示
        return {}

    def get_macro_data(self, metric_type: str) -> List[dict]:
        """获取宏观数据"""
        # 映射宏观数据类型
        endpoint_map = {
            "lpr": "cn/macro/lpr",
            "cpi": "cn/macro/cpi",
            "ppi": "cn/macro/ppi",
            "pmi": "cn/macro/pmiManuf",
            "m2": "cn/macro/m2",
        }

        endpoint = endpoint_map.get(metric_type)
        if not endpoint:
            return []

        result = self._fetch(endpoint, {}, cache_type="daily")

        if result and result.get("code") == 1:
            return result.get("data", [])
        return []

    # ==================== 资金流向接口 ====================

    def get_fund_flow_stock(self, symbol: str) -> List[dict]:
        """获取个股资金流向"""
        result = self._fetch(
            "cn/company/fund-flow",
            {"stockCode": symbol},
            cache_type="realtime"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_fund_flow_index(self, index_code: str) -> List[dict]:
        """获取指数资金流向"""
        result = self._fetch(
            "cn/index/fund-flow",
            {"indexCode": index_code},
            cache_type="realtime"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_fund_flow_industry(self, industry_code: str = None) -> List[dict]:
        """获取行业资金流向"""
        params = {}
        if industry_code:
            params["industryCode"] = industry_code
        result = self._fetch("cn/industry/fund-flow", params, cache_type="realtime")
        return result.get("data", []) if result and result.get("code") == 1 else []

    # ==================== 行业板块接口 ====================

    def get_industry_list(self) -> List[dict]:
        """获取行业列表"""
        result = self._fetch("cn/industry/basic-info", {}, cache_type="daily")
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_industry_kline(self, industry_code: str, start_date: str, end_date: str) -> List[dict]:
        """获取行业K线数据"""
        result = self._fetch(
            "cn/industry/k-line",
            {"industryCode": industry_code, "startDate": start_date, "endDate": end_date},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_industry_stocks(self, industry_code: str) -> List[dict]:
        """获取行业成分股"""
        result = self._fetch(
            "cn/industry/constituents",
            {"industryCode": industry_code},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_industry_valuation(self, industry_code: str) -> dict:
        """获取行业估值数据"""
        result = self._fetch(
            "cn/industry/valuation",
            {"industryCode": industry_code},
            cache_type="daily"
        )
        return result.get("data", [])[0] if result and result.get("code") == 1 and result.get("data") else {}

    # ==================== 指数接口 ====================

    def get_index_list(self) -> List[dict]:
        """获取指数列表"""
        result = self._fetch("cn/index/basic-info", {}, cache_type="daily")
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_index_kline(self, index_code: str, start_date: str, end_date: str) -> List[dict]:
        """获取指数K线数据"""
        result = self._fetch(
            "cn/index/k-line",
            {"indexCode": index_code, "startDate": start_date, "endDate": end_date},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_index_constituents(self, index_code: str) -> List[dict]:
        """获取指数成分股"""
        result = self._fetch(
            "cn/index/constituents",
            {"indexCode": index_code},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    # ==================== 特殊数据接口 ====================

    def get_dragon_tiger(self, symbol: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """获取龙虎榜数据 - ⚠️ API可用但通常无数据"""
        from datetime import datetime, timedelta
        # 默认查询最近1年的数据
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        result = self._fetch(
            "cn/company/trading-abnormal",
            {
                "stockCode": symbol,
                "startDate": start_date,
                "endDate": end_date
            },
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_block_deal(self, symbol: str) -> List[dict]:
        """获取大宗交易数据 - ⚠️ 理杏仁免费版不提供此数据"""
        # 理杏仁免费版不提供此接口
        return []

    def get_equity_pledge(self, symbol: str) -> List[dict]:
        """获取股权质押数据 - ⚠️ 理杏仁免费版不提供此数据"""
        # 理杏仁免费版不提供此接口
        return []

    # ==================== 股东信息接口 ====================

    def get_shareholders(self, symbol: str) -> List[dict]:
        """获取股东信息 - ⚠️ 理杏仁免费版不提供此数据"""
        # 理杏仁免费版不提供此接口
        return []

    def get_shareholders_count(self, symbol: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """获取股东人数 - ✅ 可用"""
        from datetime import datetime, timedelta
        # 默认查询最近1年的数据
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        result = self._fetch(
            "cn/company/shareholders-num",  # 正确的API路径
            {
                "stockCode": symbol,
                "startDate": start_date,
                "endDate": end_date
            },
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_executive_shareholding(self, symbol: str) -> List[dict]:
        """获取高管增减持 - ⚠️ 理杏仁免费版不提供此数据"""
        # 理杏仁免费版不提供此接口
        return []

    def get_major_shareholder_change(self, symbol: str) -> List[dict]:
        """获取大股东增减持 - ⚠️ 理杏仁免费版不提供此数据"""
        # 理杏仁免费版不提供此接口
        return []

    # ==================== 分红配股接口 ====================

    def get_dividend(self, symbol: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """获取分红送配数据 - ✅ 可用"""
        from datetime import datetime, timedelta
        # 默认查询最近3年的数据
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*3)).strftime("%Y-%m-%d")
        
        result = self._fetch(
            "cn/company/dividend",  # 正确的API路径
            {
                "stockCode": symbol,
                "startDate": start_date,
                "endDate": end_date
            },
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_equity_change(self, symbol: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """获取股本变动数据 - ✅ 可用"""
        from datetime import datetime, timedelta
        # 默认查询最近3年的数据
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*3)).strftime("%Y-%m-%d")
        
        result = self._fetch(
            "cn/company/equity-change",  # 正确的API路径
            {
                "stockCode": symbol,
                "startDate": start_date,
                "endDate": end_date
            },
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    # ==================== 其他数据接口 ====================

    def get_revenue_structure(self, symbol: str) -> List[dict]:
        """获取营收构成"""
        result = self._fetch(
            "cn/company/revenue-structure",
            {"stockCode": symbol},
            cache_type="financial"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_operation_data(self, symbol: str) -> List[dict]:
        """获取经营数据"""
        result = self._fetch(
            "cn/company/operation-data",
            {"stockCode": symbol},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_related_industry(self, symbol: str) -> List[dict]:
        """获取股票所属行业"""
        result = self._fetch(
            "cn/company/related-industry",
            {"stockCode": symbol},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_related_index(self, symbol: str) -> List[dict]:
        """获取股票所属指数"""
        result = self._fetch(
            "cn/company/related-index",
            {"stockCode": symbol},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_announcement(self, symbol: str, limit: int = 10) -> List[dict]:
        """获取公告数据"""
        result = self._fetch(
            "cn/company/announcement",
            {"stockCode": symbol, "limit": limit},
            cache_type="daily"
        )
        return result.get("data", []) if result and result.get("code") == 1 else []

    def get_hot_data(self, symbol: str) -> dict:
        """获取热度数据"""
        result = self._fetch(
            "cn/company/hot-data",
            {"stockCode": symbol},
            cache_type="realtime"
        )
        return result.get("data", [])[0] if result and result.get("code") == 1 and result.get("data") else {}
