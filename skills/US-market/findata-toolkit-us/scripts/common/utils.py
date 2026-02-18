"""
金融数据工具包共享工具
所有脚本通用函数。
"""
import json
import sys
import time
import functools
from datetime import datetime, date
from typing import Any


# ---------------------------------------------------------------------------
# 输出助手
# ---------------------------------------------------------------------------

class JSONEncoder(json.JSONEncoder):
    """自定义编码器，处理日期、numpy 类型等。"""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        try:
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.bool_):
                return bool(obj)
        except ImportError:
            pass
        try:
            import pandas as pd
            if isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            if pd.isna(obj):
                return None
        except ImportError:
            pass
        return super().default(obj)


def output_json(data: Any, pretty: bool = True) -> str:
    """将数据序列化为 JSON 并输出到标准输出。"""
    text = json.dumps(data, cls=JSONEncoder, indent=2 if pretty else None,
                      ensure_ascii=False)
    print(text)
    return text


def output_table(headers: list[str], rows: list[list], title: str = ""):
    """输出格式化文本表格。"""
    try:
        from tabulate import tabulate
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}")
        print(tabulate(rows, headers=headers, tablefmt="pipe",
                        floatfmt=".2f"))
    except ImportError:
        if title:
            print(f"\n--- {title} ---")
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for row in rows:
            print(" | ".join(str(c) for c in row))


def error_exit(message: str, code: int = 1):
    """输出错误信息并退出。"""
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# 速率限制
# ---------------------------------------------------------------------------

def rate_limit(calls_per_second: float = 2.0):
    """限速装饰器。"""
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_call = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)

        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 安全数值助手
# ---------------------------------------------------------------------------

def safe_div(a, b, default=None):
    """安全除法，b 为 0 或任一值为 None 时返回 default。"""
    if a is None or b is None:
        return default
    try:
        if float(b) == 0:
            return default
        return float(a) / float(b)
    except (ValueError, TypeError):
        return default


def safe_float(val, default=None):
    """安全转换为 float，失败时返回 default。"""
    if val is None:
        return default
    try:
        import math
        result = float(val)
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except (ValueError, TypeError):
        return default


def pct(val, decimals=2):
    """将小数格式化为百分比字符串。"""
    if val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"


def safe_pe(market_cap, net_profit, default=None):
    """安全PE计算，净利润为非正时返回default。

    PE = 市值 / 净利润，当净利润<=0时返回None（表示亏损，PE无意义）
    """
    if market_cap is None or net_profit is None:
        return default
    try:
        mc = float(market_cap)
        np = float(net_profit)
        if np <= 0:
            return default
        if mc <= 0:
            return default
        return mc / np
    except (ValueError, TypeError):
        return default


def safe_financial_value(value, default=None, min_value=0):
    """安全金融数值校验，确保数值大于min_value。

    适用于市值、价格、成交量等不能为负或零的指标。
    """
    if value is None:
        return default
    try:
        val = float(value)
        if val <= min_value:
            return default
        return val
    except (ValueError, TypeError):
        return default


def safe_change_pct(current, previous, default=None, max_bound=10, min_bound=-0.9):
    """安全涨跌幅计算，包含边界检查。

    涨跌幅 = (当前价 - 前价) / 前价
    异常值（如超过1000%涨幅或90%跌幅）返回default。
    """
    if current is None or previous is None:
        return default
    try:
        curr = float(current)
        prev = float(previous)
        if prev <= 0:
            return default
        change = (curr - prev) / prev
        if change > max_bound or change < min_bound:
            return default
        return change
    except (ValueError, TypeError):
        return default
