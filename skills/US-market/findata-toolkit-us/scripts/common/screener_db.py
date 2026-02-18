import duckdb
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

class ScreenerDB:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            cache_dir = base_dir / ".cache"
            cache_dir.mkdir(exist_ok=True)
            db_path = str(cache_dir / "screener.db")
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    stockCode VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    industry VARCHAR,
                    area VARCHAR,
                    market_cap DOUBLE,
                    pe_ttm DOUBLE,
                    pb DOUBLE,
                    last_update TIMESTAMP
                )
            """)

    def sync_from_lixinger(self, client):
        """
        从理杏仁同步基础指标数据（通常每天执行一次）。
        """
        # 1. 获取 A 股所有股票基础信息
        basic_res = client.fetch("us/company", {})
        if not basic_res or basic_res.get('code') != 1:
            return False
        
        # 2. 获取实时行情（含 PE/PB/市值）
        # 注意：这里需要根据实际 API 调整，假设 cn/company/fundamental/non_financial 支持批量
        # 或者我们分批获取
        
        # 简化版：先存入基础信息
        with duckdb.connect(self.db_path) as conn:
            now = datetime.now()
            for item in basic_res['data']:
                conn.execute("""
                    INSERT OR REPLACE INTO stocks (stockCode, name, industry, last_update)
                    VALUES (?, ?, ?, ?)
                """, [item.get('stockCode'), item.get('name'), item.get('industry'), now])
        
        return True

    def query(self, where_clause: str = None, limit: int = 50):
        """
        执行 SQL 风格的筛选。
        Example: pe_ttm < 20 AND industry = '白酒'
        """
        sql = "SELECT * FROM stocks"
        if where_clause:
            # 使用参数化查询防止SQL注入
            sql += " WHERE " + ", ".join([f"{k} = ?" for k in where_clause.keys()])
            params = list(where_clause.values())
        sql += f" LIMIT {limit}"
        
        try:
            with duckdb.connect(self.db_path) as conn:
                df = conn.execute(sql).fetchdf()
                return df.to_dict(orient='records')
        except Exception as e:
            return {"error": str(e)}
