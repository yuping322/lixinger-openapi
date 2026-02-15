import os
import json
import duckdb
from datetime import datetime, timedelta
from pathlib import Path

class CacheManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to a .cache directory in the skill folder
            base_dir = Path(__file__).resolve().parent.parent.parent
            cache_dir = base_dir / ".cache"
            cache_dir.mkdir(exist_ok=True)
            db_path = str(cache_dir / "api_cache.db")
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with duckdb.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS api_cache (
                        key VARCHAR PRIMARY KEY,
                        suffix VARCHAR,
                        params VARCHAR,
                        response VARCHAR,
                        timestamp TIMESTAMP,
                        expiry_timestamp TIMESTAMP
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS session_lists (
                        name VARCHAR PRIMARY KEY,
                        stock_codes VARCHAR,
                        timestamp TIMESTAMP
                    )
                """)
        except Exception:
            # Fallback if DuckDB has issues (e.g. concurrent access)
            pass

    def _generate_key(self, suffix, params):
        # Sort params to ensure consistency
        params_str = json.dumps(params, sort_keys=True)
        return f"{suffix}:{params_str}"

    def get(self, suffix, params, max_age_days=1):
        key = self._generate_key(suffix, params)
        try:
            with duckdb.connect(self.db_path) as conn:
                res = conn.execute("SELECT response, timestamp FROM api_cache WHERE key = ?", [key]).fetchone()
                if res:
                    response_str, timestamp = res
                    # DuckDB timestamp might be datetime already
                    if datetime.now() - timestamp < timedelta(days=max_age_days):
                        return json.loads(response_str)
        except Exception:
            pass
        return None

    def set(self, suffix, params, response, expiry_days=1):
        key = self._generate_key(suffix, params)
        response_str = json.dumps(response)
        now = datetime.now()
        expiry = now + timedelta(days=expiry_days)
        
        try:
            with duckdb.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO api_cache (key, suffix, params, response, timestamp, expiry_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, [key, suffix, json.dumps(params), response_str, now, expiry])
        except Exception:
            pass

    def save_list(self, name, stock_codes):
        try:
            with duckdb.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO session_lists (name, stock_codes, timestamp)
                    VALUES (?, ?, ?)
                """, [name, json.dumps(stock_codes), datetime.now()])
        except Exception:
            pass

    def get_list(self, name):
        try:
            with duckdb.connect(self.db_path) as conn:
                res = conn.execute("SELECT stock_codes FROM session_lists WHERE name = ?", [name]).fetchone()
                if res:
                    return json.loads(res[0])
        except Exception:
            pass
        return None

    def clear(self):
        try:
            with duckdb.connect(self.db_path) as conn:
                conn.execute("DELETE FROM api_cache")
        except Exception:
            pass
