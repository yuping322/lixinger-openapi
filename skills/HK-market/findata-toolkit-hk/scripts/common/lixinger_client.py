import os
import sys
import json
import pandas as pd
from pathlib import Path
from .config import get_lixinger_token, get_metadata_path
from .cache import CacheManager

# 尝试导入 lixinger_openapi，如果没有则报错
try:
    from lixinger_openapi.query import query_json
    from lixinger_openapi.token import set_token
except ImportError:
    # 动态添加路径以防万一
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))
    from lixinger_openapi.query import query_json
    from lixinger_openapi.token import set_token

class LixingerClient:
    def __init__(self):
        self.token = get_lixinger_token()
        if self.token:
            set_token(self.token, write_token=False)
        self.cache = CacheManager()
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        meta_path = get_metadata_path()
        if meta_path and meta_path.exists():
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def fetch(self, suffix: str, params: dict, cache_enabled: bool = True, limit: int = 1000) -> dict:
        """
        获取理杏仁数据，自动处理：
        1. 缓存加载与更新
        2. 元数据驱动的单位换算
        3. Token 注入
        """
        params = dict(params)
        if "token" not in params:
            params["token"] = self.token

        # Normalize suffix for metadata lookup
        lookup_suffix = suffix.replace('.', '/')
        api_meta = self.metadata.get(lookup_suffix)

        # 尝试缓存
        result = None
        if cache_enabled:
            max_age_days = 1
            if api_meta:
                freq = api_meta.get('update_frequency', 'daily')
                if freq == 'realtime': max_age_days = 0.04
                elif freq == 'weekly': max_age_days = 7
                elif freq == 'monthly': max_age_days = 30
            result = self.cache.get(suffix, params, max_age_days=max_age_days)

        if not result:
            result = query_json(suffix, params)
            if cache_enabled and result and result.get('code') == 1:
                expiry_days = 1
                if api_meta:
                    freq = api_meta.get('update_frequency', 'daily')
                    if freq == 'realtime': expiry_days = 0.04
                    elif freq == 'weekly': expiry_days = 7
                    elif freq == 'monthly': expiry_days = 30
                self.cache.set(suffix, params, result, expiry_days=expiry_days)

        # 应用单位换算
        if api_meta and result and result.get('code') == 1 and isinstance(result.get('data'), list):
            conversions = api_meta.get('conversions', [])
            for item in result['data']:
                for conv in conversions:
                    field = conv['field']
                    if field in item and item[field] is not None:
                        try:
                            val = float(item[field])
                            if conv['operation'] == 'div': val = val / conv['factor']
                            elif conv['operation'] == 'mul': val = val * conv['factor']
                            if 'round' in conv: val = round(val, conv['round'])
                            item[conv.get('name', field)] = val
                        except (ValueError, TypeError):
                            pass

        # 截断
        if result and result.get('code') == 1 and isinstance(result.get('data'), list):
            if len(result['data']) > limit:
                result['data'] = result['data'][:limit]
                result['_note'] = f"Truncated to {limit} rows."

        return result
