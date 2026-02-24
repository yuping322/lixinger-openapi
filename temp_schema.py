import json
import sys
from lixinger_openapi.query import query_json

suffixes = [
    ("cn/index", {"stockCodes": ["000001"]}),
    ("cn/index/fundamental", {"stockCodes": ["000001"], "metricsList": ["pe_ttm"], "startDate": "2024-01-01"}),
    ("cn/index/valuation", {"stockCodes": ["000001"], "startDate": "2024-01-01"}),
    ("cn/index/constituents", {"stockCodes": ["000001"], "date": "2024-01-01"}),
    ("cn/industry", {"stockCodes": ["110000"]}),
    ("cn/industry/fundamental", {"stockCodes": ["110000"], "metricsList": ["pe_ttm"], "startDate": "2024-01-01"}),
    ("cn/industry/valuation", {"stockCodes": ["110000"], "startDate": "2024-01-01"}),
    ("cn/industry/constituents", {"stockCodes": ["110000"], "date": "2024-01-01"}),
]

for suffix, params in suffixes:
    try:
        res = query_json(suffix, params)
        if isinstance(res, list) and len(res) > 0:
            print(f"--- {suffix} ---")
            print(json.dumps(res[0], indent=2, ensure_ascii=False))
        elif isinstance(res, dict) and "data" in res and len(res["data"]) > 0:
            print(f"--- {suffix} ---")
            print(json.dumps(res["data"][0], indent=2, ensure_ascii=False))
        elif isinstance(res, dict) and "dataList" in res and len(res["dataList"]) > 0:
            print(f"--- {suffix} ---")
            print(json.dumps(res["dataList"][0], indent=2, ensure_ascii=False))
        else:
            print(f"--- {suffix} --- NO DATA OR DIFF FORMAT")
            print(res)
    except Exception as e:
         print(f"--- {suffix} --- ERROR: {e}")
