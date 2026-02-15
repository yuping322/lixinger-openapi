# -*- coding: utf-8 -*-
"""
Quickstart guide for lixinger-openapi.
This script demonstrates the basic usage of the library to fetch stock and index data.
"""

from lixinger_openapi.query import query_json, query_dataframe
import pandas as pd

def run_quickstart():
    print("--- 1. Querying Bank Companies in China (DataFrame) ---")
    # Example: Query all banks in A-share market
    # url_suffix can Use '.' as a separator instead of '/'
    rlt = query_dataframe("cn.company", {"fsTableType": "bank"})
    
    # Lixinger API typically returns code 1 for success
    if rlt['code'] == 1:
        df = rlt['data']
        print(f"Successfully fetched {len(df)} banks.")
        print(df[['stockCode', 'name']].head())
    else:
        print(f"Error: {rlt['msg']} (Code: {rlt['code']})")

    print("\n--- 2. Querying Index Constituents (JSON) ---")
    # Example: Query constituents of SSE 50 Index (000016) on a specific date
    params = {
        "date": "2023-12-29",
        "stockCodes": ["000016"]
    }
    rlt_json = query_json("cn/index/constituents", params)
    
    if rlt_json.get('code') == 1:
        data = rlt_json.get('data', [])
        print(f"Successfully fetched constituents for SSE 50.")
        print(f"First 5 constituents: {[item['stockCode'] for item in data[:5]]}")
    else:
        print(f"Error: {rlt_json.get('message')} (Code: {rlt_json.get('code')})")

    print("\n--- 3. Querying Index Fundamental Data (DataFrame) ---")
    # Example: Query PE (TTM) for SSE 50
    params = {
        "date": "2024-12-10",
        "stockCodes": ["000016"],
        "metricsList": ["pe_ttm.mcw", "mc"]
    }
    rlt_fund = query_dataframe("cn.index.fundamental", params)
    
    if rlt_fund['code'] == 1:
        df_fund = rlt_fund['data']
        print("Fundamental Data:")
        print(df_fund)
    else:
        print(f"Error: {rlt_fund['msg']} (Code: {rlt_fund['code']})")

if __name__ == "__main__":
    try:
        run_quickstart()
    except Exception as e:
        print(f"Caught an exception: {e}")
        print("\nTip: Make sure your token.cfg file contains a valid token.")
