import os
import sys
from pathlib import Path
import pandas as pd
import json
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token

def get_lixinger_token() -> str:
    """Find token in environment or token.cfg in parent directories."""
    # 1. Environment variable
    token = os.getenv("LIXINGER_TOKEN")
    if token:
        return token
    
    # 2. Search upwards for token.cfg
    curr = Path(os.getcwd()).resolve()
    for _ in range(5): # Check up to 5 levels
        cfg_path = curr / "token.cfg"
        if cfg_path.exists():
            try:
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        # Handle configparser format if present, else raw string
                        if content.startswith("["):
                            import configparser
                            config = configparser.ConfigParser()
                            config.read_string(content)
                            return config.get("lixinger", "token", fallback="")
                        return content
            except Exception:
                pass
        curr = curr.parent
    return ""

def init_lixinger():
    """Initialize Lixinger API with token."""
    token = get_lixinger_token()
    if not token:
        print("Warning: Lixinger token not found. Please set LIXINGER_TOKEN or create token.cfg.", file=sys.stderr)
        return False
    set_token(token, write_token=False)
    return True

def get_a_share_list():
    """Get list of all A-share stocks."""
    # API: cn/company/basic-info (or custom query if basic-info is heavy)
    # Using specific optimized query or basic info
    payload = {
        "stockCodes": [] # Empty list usually returns all or needs specific handling. 
        # Lixinger typically requires codes. To get ALL, we might need a specific endpoint or index constituents.
    }
    # For now, let's assume we use a known index or user provided codes. 
    # But often users want "all". Lixinger 'cn/company/basic-info' supports getting all? 
    # Let's check api_catalog. No, usually you query by indices.
    pass

def get_stock_price(stock_code, start_date=None, end_date=None, adjust="qfq", limit=None):
    """
    Get daily stock price (K-line).
    
    Args:
        stock_code (str): Stock code (e.g., "600519").
        start_date (str): "YYYY-MM-DD".
        end_date (str): "YYYY-MM-DD".
        adjust (str): "qfq" (forward), "hfq" (backward), "none".
        limit (int): Max rows to return.
    """
    if not init_lixinger(): return None
    
    # Map adjust to Lixinger type
    # qfq -> lxr_fc_rights (Lixinger forward), hfq -> bc_rights, none -> ex_rights
    adjust_map = {
        "qfq": "lxr_fc_rights", 
        "hfq": "bc_rights", 
        "none": "ex_rights"
    }
    adj_type = adjust_map.get(adjust, "lxr_fc_rights")
    
    params = {
        "stockCode": stock_code,
        "type": adj_type,
    }
    
    if start_date: params["startDate"] = start_date
    if end_date: params["endDate"] = end_date
    if limit: params["limit"] = limit
    
    # API: cn/company/candlestick (or k-line)
    # Lixinger endpoint often uses 'k-line' in URL but 'candlestick' in some docs.
    # api_catalog says 'cn/company/k-line'.
    res = query_json("cn/company/candlestick", params)
    
    if res['code'] == 1:
        df = pd.DataFrame(res['data'])
        if not df.empty:
            # Standardize columns if needed
            pass
        return df
    else:
        print(f"Error fetching price for {stock_code}: {res}", file=sys.stderr)
        return None

def get_fundamentals(stock_code, date=None, metrics=None):
    """
    Get fundamental data (PE, PB, Market Cap) for non-financial companies.
    
    Args:
        stock_code (str): Stock code.
        date (str): "YYYY-MM-DD".
        metrics (list): List of metrics. Defaults to ["pe_ttm", "pb", "mc"].
    """
    if not init_lixinger(): return None
    
    if metrics is None:
        metrics = ["pe_ttm", "pb", "mc"]
    
    params = {
        "stockCodes": [stock_code],
        "metricsList": metrics,
    }
    if date: params["date"] = date
    
    # Defaulting to non_financial for now. Real implementation should check company type.
    res = query_json("cn/company/fundamental/non_financial", params)
    
    if res['code'] == 1:
        df = pd.DataFrame(res['data'])
        return df
    else:
        print(f"Error fetching fundamentals for {stock_code}: {res.get('msg')}", file=sys.stderr)
        return None

def get_financials(stock_code, date=None, type="q", metrics=None):
    """
    Get financial statement data.
    
    Args:
        stock_code (str): Stock code.
        date (str): "YYYY-MM-DD" (standardDate).
        type (str): "q" (quarterly), "a" (annual).
        metrics (list): List of metrics (e.g. ["q.profitStatement.oi"]). REQUIRED.
    """
    if not init_lixinger(): return None
    
    if not metrics:
        print("Error: 'metrics' list is required for get_financials.", file=sys.stderr)
        return None

    params = {
        "stockCodes": [stock_code],
        "reportType": type,
        "metricsList": metrics
    }
    if date: params["date"] = date # Lixinger API typically uses 'date' for point-in-time or 'startDate'/'endDate' range
    # Check if 'date' in financial-statement means report date or valid date. Use 'date' for point query.
    
    res = query_json("cn/company/financial-statement", params)
    
    if res['code'] == 1:
        df = pd.DataFrame(res['data'])
        return df
    else:
        print(f"Error fetching financials for {stock_code}: {res.get('msg')}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if init_lixinger():
        print(">>> Testing Price Data (000001)")
        df_price = get_stock_price("000001", start_date="2024-01-01", end_date="2024-01-10")
        if df_price is not None:
            print(df_price.head())
            
        print("\n>>> Testing Fundamentals (600519)")
        df_fund = get_fundamentals("600519", date="2024-01-05")
        if df_fund is not None:
            print(df_fund)

        # Note: Financials require specific metrics which we don't hardcode to avoid guessing errors without metadata.
