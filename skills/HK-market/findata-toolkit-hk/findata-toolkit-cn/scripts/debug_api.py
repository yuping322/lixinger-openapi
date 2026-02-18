import sys
import os
import json
from pathlib import Path

# Add scripts to path
sys.path.insert(0, os.path.dirname(__file__))

from common.lixinger_client import LixingerClient

def debug():
    client = LixingerClient()
    
    print("--- cn/company/basic-info ---")
    res1 = client.fetch("hk/company/basic-info", {"stockCodes": ["600519"]})
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    
    print("\n--- cn/company/related-industry ---")
    res1_5 = client.fetch("hk/company/related-industry", {"stockCodes": ["600519"]})
    print(json.dumps(res1_5, indent=2, ensure_ascii=False))

    print("\n--- cn/company/fundamental/non_financial ---")
    res2 = client.fetch("hk/company/fundamental/non_financial", {
        "stockCodes": ["600519"], 
        "metricsList": ["pe_ttm", "pb", "mc"],
        "limit": 1
    })
    print(json.dumps(res2, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    debug()
