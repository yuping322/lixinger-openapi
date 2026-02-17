import os
import json
from datetime import datetime, timedelta

class UnifiedCache:
    """统一缓存管理器（替换各模块独立实现）"""
    def __init__(self, cache_dir='.cache', ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def get(self, key):
        """获取缓存（自动处理过期）"""
        path = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(path):
            return None

        with open(path) as f:
            data = json.load(f)
            if datetime.now() > datetime.fromisoformat(data['expire_at']):
                os.remove(path)
                return None
            return data['value']

    def set(self, key, value):
        """设置缓存"""
        path = os.path.join(self.cache_dir, f"{key}.json")
        data = {
            'value': value,
            'expire_at': (datetime.now() + self.ttl).isoformat()
        }
        with open(path, 'w') as f:
            json.dump(data, f)