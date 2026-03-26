#!/usr/bin/env python3
"""Analyze saved Lixinger screener results and run a quick forward test."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import statistics
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_RESULTS_DIR = ROOT / "url_results"
DEFAULT_QUERY_TOOL = (
    ROOT / ".claude" / "plugins" / "query_data" / "lixinger-api-docs" / "scripts" / "query_tool.py"
)
DEFAULT_CACHE_DIR = ROOT / ".cache" / "screener_backtest"


def parse_date(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        if math.isnan(value):
            return None
        return float(value)
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


@dataclass
class ScreenerRecord:
    path: Path
    screener_id: str | None
    area: str
    name: str
    description: str | None
    total: int
    latest_time: str | None
    latest_quarter: str | None
    rows: list[dict[str, Any]]
    codes: list[str]
    code_set: set[str]


def infer_area_from_name(path: Path) -> str:
    parts = path.stem.split("_")
    if len(parts) >= 3:
        return parts[1]
    return "unknown"


def load_screeners(results_dir: Path, area: str | None = None) -> list[ScreenerRecord]:
    records: list[ScreenerRecord] = []
    for path in sorted(results_dir.glob("screener_*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows = data.get("rows")
        if not isinstance(rows, list):
            continue
        area_code = infer_area_from_name(path)
        if area and area_code != area:
            continue
        codes = [row["代码"] for row in rows if row.get("代码")]
        records.append(
            ScreenerRecord(
                path=path,
                screener_id=data.get("screenerId"),
                area=area_code,
                name=data.get("screenerName") or path.stem,
                description=data.get("screenerDescription"),
                total=int(data.get("total", len(codes) or 0)),
                latest_time=data.get("latestTime"),
                latest_quarter=data.get("latestQuarter"),
                rows=rows,
                codes=codes,
                code_set=set(codes),
            )
        )
    return records


def top_consensus(
    records: list[ScreenerRecord],
    narrow_max_results: int,
    limit: int,
) -> list[tuple[int, str, str, str, list[str]]]:
    narrow = [record for record in records if 0 < record.total <= narrow_max_results]
    code_counts: Counter[str] = Counter()
    name_map: dict[str, str] = {}
    industry_map: dict[str, str] = {}
    memberships: dict[str, list[str]] = {}

    for record in narrow:
        for row in record.rows:
            code = row.get("代码")
            if not code:
                continue
            code_counts[code] += 1
            name_map[code] = row.get("公司名称") or ""
            industry_map[code] = row.get("行业") or ""
            memberships.setdefault(code, []).append(record.name)

    ranked: list[tuple[int, str, str, str, list[str]]] = []
    for code, count in code_counts.most_common(limit):
        ranked.append((count, code, name_map.get(code, ""), industry_map.get(code, ""), memberships[code]))
    return ranked


def similar_pairs(records: list[ScreenerRecord], max_results: int, limit: int) -> list[tuple[float, int, ScreenerRecord, ScreenerRecord]]:
    filtered = [record for record in records if 0 < record.total <= max_results]
    pairs: list[tuple[float, int, ScreenerRecord, ScreenerRecord]] = []
    for idx, left in enumerate(filtered):
        for right in filtered[idx + 1 :]:
            intersection = len(left.code_set & right.code_set)
            if intersection == 0:
                continue
            union = len(left.code_set | right.code_set)
            jaccard = intersection / union
            pairs.append((jaccard, intersection, left, right))
    pairs.sort(key=lambda item: (item[0], item[1], -abs(item[2].total - item[3].total)), reverse=True)
    return pairs[:limit]


def negative_pe_screeners(records: list[ScreenerRecord]) -> list[tuple[ScreenerRecord, int, int]]:
    flagged: list[tuple[ScreenerRecord, int, int]] = []
    for record in records:
        negative_rows = 0
        observed_rows = 0
        for row in record.rows:
            pe_values = [safe_float(row.get("pm.pe_ttm")), safe_float(row.get("pm.d_pe_ttm"))]
            pe_values = [value for value in pe_values if value is not None]
            if not pe_values:
                continue
            observed_rows += 1
            if any(value < 0 for value in pe_values):
                negative_rows += 1
        if negative_rows:
            flagged.append((record, negative_rows, observed_rows))
    flagged.sort(key=lambda item: (item[1] / max(item[2], 1), item[1]), reverse=True)
    return flagged


def print_overview(args: argparse.Namespace) -> int:
    results_dir = Path(args.results_dir)
    records = load_screeners(results_dir, area=args.area)
    if not records:
        print(f"No screener result JSON files found in {results_dir}.", file=sys.stderr)
        return 1

    zero_count = sum(1 for record in records if record.total == 0)
    narrow_count = sum(1 for record in records if 0 < record.total <= args.narrow_max_results)
    broad_count = sum(1 for record in records if record.total >= args.broad_min_results)
    latest_times = Counter(record.latest_time for record in records)

    print("== Screener Overview ==")
    print(f"Results dir: {results_dir}")
    print(f"Area: {args.area or 'all'}")
    print(f"Loaded screeners: {len(records)}")
    print(f"Narrow screeners (1-{args.narrow_max_results}): {narrow_count}")
    print(f"Broad pools (>={args.broad_min_results}): {broad_count}")
    print(f"Zero-result screeners: {zero_count}")
    print(f"Latest times: {dict(sorted(latest_times.items()))}")

    print("\n== Smallest Screeners ==")
    for record in sorted(records, key=lambda item: item.total)[: args.limit]:
        print(f"{record.total:4d} | {record.name} | {record.path.name}")

    print("\n== Largest Screeners ==")
    for record in sorted(records, key=lambda item: item.total, reverse=True)[: args.limit]:
        print(f"{record.total:4d} | {record.name} | {record.path.name}")

    print(f"\n== Consensus Stocks Within Narrow Screeners (<= {args.narrow_max_results}) ==")
    for count, code, name, industry, memberships in top_consensus(records, args.narrow_max_results, args.limit):
        joined = " | ".join(memberships[:6])
        suffix = "" if len(memberships) <= 6 else f" | ... (+{len(memberships) - 6})"
        print(f"{count:2d} | {code} | {name} | {industry} | {joined}{suffix}")

    print(f"\n== Most Similar Screener Pairs (<= {args.pair_max_results} results) ==")
    for jaccard, intersection, left, right in similar_pairs(records, args.pair_max_results, args.limit):
        print(
            f"{jaccard:.3f} | inter={intersection:3d} | "
            f"{left.name} ({left.total}) <-> {right.name} ({right.total})"
        )

    print("\n== Screeners With Negative PE Rows ==")
    flagged = negative_pe_screeners(records)
    if not flagged:
        print("None")
    else:
        for record, negative_rows, observed_rows in flagged[: args.limit]:
            ratio = negative_rows / max(observed_rows, 1)
            print(
                f"{negative_rows:3d}/{observed_rows:3d} ({ratio:.1%}) | "
                f"{record.name} | {record.path.name}"
            )

    return 0


def normalize_stock_code(code: str) -> str:
    return code.split(".", 1)[0]


def run_query_tool(
    query_tool: Path,
    suffix: str,
    params: dict[str, Any],
    columns: list[str],
    limit: int = 5000,
) -> str:
    cmd = [
        sys.executable,
        str(query_tool),
        "--suffix",
        suffix,
        "--params",
        json.dumps(params, ensure_ascii=False),
        "--columns",
        ",".join(columns),
        "--limit",
        str(limit),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "Unknown query_tool error")
    return completed.stdout


def parse_csv_output(raw_text: str) -> list[dict[str, str]]:
    lines = [line for line in raw_text.splitlines() if line.strip() and not line.startswith("# NOTE:")]
    if not lines:
        return []
    reader = csv.DictReader(io.StringIO("\n".join(lines)))
    return list(reader)


def query_candlestick(
    query_tool: Path,
    cache_dir: Path,
    suffix: str,
    stock_code: str,
    kind: str,
    start_date: str,
    end_date: str,
) -> list[dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{suffix.replace('.', '_')}_{stock_code}_{kind}_{start_date}_{end_date}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    params = {
        "stockCode": stock_code,
        "type": kind,
        "startDate": start_date,
        "endDate": end_date,
    }
    raw = run_query_tool(
        query_tool=query_tool,
        suffix=suffix,
        params=params,
        columns=["date", "stockCode", "open", "close"],
        limit=5000,
    )
    rows = parse_csv_output(raw)
    normalized = [
        {
            "date": row["date"][:10],
            "stockCode": row.get("stockCode", stock_code),
            "open": safe_float(row.get("open")),
            "close": safe_float(row.get("close")),
        }
        for row in rows
        if row.get("date")
    ]
    cache_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized


def first_date_after(series: list[dict[str, Any]], threshold: date) -> str | None:
    for row in sorted(series, key=lambda item: item["date"]):
        current = parse_date(row["date"])
        if current > threshold:
            return row["date"]
    return None


def first_row_on_or_after(series: list[dict[str, Any]], threshold_date: str) -> dict[str, Any] | None:
    for row in sorted(series, key=lambda item: item["date"]):
        if row["date"] >= threshold_date:
            return row
    return None


def build_selected_records(records: list[ScreenerRecord], args: argparse.Namespace) -> list[ScreenerRecord]:
    selected = []
    for record in records:
        if args.area and record.area != args.area:
            continue
        if args.max_results is not None and record.total > args.max_results:
            continue
        if args.min_results is not None and record.total < args.min_results:
            continue
        if args.screener_id and record.screener_id != args.screener_id:
            continue
        if args.name_contains and args.name_contains not in record.name:
            continue
        selected.append(record)
    return selected


def summarize_returns(values: list[float]) -> tuple[float | None, float | None, float | None]:
    if not values:
        return None, None, None
    return (
        mean(values),
        statistics.median(values),
        sum(1 for value in values if value > 0) / len(values),
    )


def print_forward_test(args: argparse.Namespace) -> int:
    results_dir = Path(args.results_dir)
    query_tool = Path(args.query_tool)
    cache_dir = Path(args.cache_dir)
    records = build_selected_records(load_screeners(results_dir, area=args.area), args)
    if not records:
        print("No screeners matched the requested filters.", file=sys.stderr)
        return 1
    if not query_tool.exists():
        print(f"query_tool.py not found: {query_tool}", file=sys.stderr)
        return 1

    horizons = [int(part.strip()) for part in args.horizons.split(",") if part.strip()]
    end_date = args.end_date or date.today().isoformat()
    benchmark_series = query_candlestick(
        query_tool=query_tool,
        cache_dir=cache_dir / "benchmark",
        suffix="cn.index.candlestick",
        stock_code=args.benchmark,
        kind=args.benchmark_type,
        start_date=args.start_date,
        end_date=end_date,
    )
    if not benchmark_series:
        print("Benchmark series is empty. Check token/API permissions.", file=sys.stderr)
        return 1

    print("== Forward Test ==")
    print(f"Results dir: {results_dir}")
    print(f"Selected screeners: {len(records)}")
    print(f"Benchmark: {args.benchmark} ({args.benchmark_type})")
    print(f"Horizons: {horizons}")
    print("Assumption: buy at next trading day's open, evaluate at benchmark horizon close.")

    for record in records:
        if not record.latest_time:
            print(f"\n{record.name}: skipped (missing latestTime)")
            continue

        entry_anchor = parse_date(record.latest_time)
        benchmark_entry_date = first_date_after(benchmark_series, entry_anchor)
        if not benchmark_entry_date:
            print(f"\n{record.name}: skipped (no trading day after {record.latest_time})")
            continue

        benchmark_sorted = sorted(benchmark_series, key=lambda item: item["date"])
        benchmark_index = next(
            idx for idx, row in enumerate(benchmark_sorted) if row["date"] == benchmark_entry_date
        )
        benchmark_entry = benchmark_sorted[benchmark_index]

        stock_codes = [normalize_stock_code(code) for code in record.codes]
        if args.max_stocks_per_screener:
            stock_codes = stock_codes[: args.max_stocks_per_screener]

        stock_series_map: dict[str, list[dict[str, Any]]] = {}
        window_start = record.latest_time
        window_end = end_date
        for code in stock_codes:
            stock_series_map[code] = query_candlestick(
                query_tool=query_tool,
                cache_dir=cache_dir / "stocks",
                suffix="cn.company.candlestick",
                stock_code=code,
                kind=args.stock_type,
                start_date=window_start,
                end_date=window_end,
            )

        print(f"\n{record.name} | {record.total} stocks | file={record.path.name}")
        print(f"Screen date: {record.latest_time} | benchmark entry date: {benchmark_entry_date}")

        for horizon in horizons:
            benchmark_exit_index = benchmark_index + horizon
            if benchmark_exit_index >= len(benchmark_sorted):
                print(f"  {horizon:>3}d | skipped (not enough future benchmark bars)")
                continue

            benchmark_exit = benchmark_sorted[benchmark_exit_index]
            benchmark_return = None
            if benchmark_entry.get("open") and benchmark_exit.get("close"):
                benchmark_return = benchmark_exit["close"] / benchmark_entry["open"] - 1

            stock_returns: list[float] = []
            for code, series in stock_series_map.items():
                if not series:
                    continue
                entry_row = first_row_on_or_after(series, benchmark_entry_date)
                exit_row = first_row_on_or_after(series, benchmark_exit["date"])
                if not entry_row or not exit_row:
                    continue
                if not entry_row.get("open") or not exit_row.get("close"):
                    continue
                stock_returns.append(exit_row["close"] / entry_row["open"] - 1)

            avg_ret, median_ret, hit_rate = summarize_returns(stock_returns)
            excess = None if avg_ret is None or benchmark_return is None else avg_ret - benchmark_return
            coverage = f"{len(stock_returns)}/{len(stock_codes)}"
            print(
                f"  {horizon:>3}d | coverage={coverage:>7} | "
                f"avg={pct(avg_ret):>8} | median={pct(median_ret):>8} | "
                f"hit={pct(hit_rate):>8} | benchmark={pct(benchmark_return):>8} | excess={pct(excess):>8}"
            )

    print(
        "\nNote: if every screener file is for the current date, forward returns will be unavailable until "
        "future trading days exist. Archive a daily snapshot folder to make this genuinely out-of-sample."
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze saved screener outputs and run quick forward tests.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    overview = subparsers.add_parser("overview", help="Summarize screener output quality and overlap.")
    overview.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    overview.add_argument("--area", default="cn")
    overview.add_argument("--limit", type=int, default=10)
    overview.add_argument("--narrow-max-results", type=int, default=100)
    overview.add_argument("--broad-min-results", type=int, default=500)
    overview.add_argument("--pair-max-results", type=int, default=250)
    overview.set_defaults(func=print_overview)

    forward = subparsers.add_parser("forward-test", help="Run a quick next-day-open forward test.")
    forward.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    forward.add_argument("--area", default="cn")
    forward.add_argument("--query-tool", default=str(DEFAULT_QUERY_TOOL))
    forward.add_argument("--cache-dir", default=str(DEFAULT_CACHE_DIR))
    forward.add_argument("--screener-id")
    forward.add_argument("--name-contains")
    forward.add_argument("--min-results", type=int)
    forward.add_argument("--max-results", type=int, default=100)
    forward.add_argument("--max-stocks-per-screener", type=int, default=50)
    forward.add_argument("--benchmark", default="000300")
    forward.add_argument("--benchmark-type", default="normal")
    forward.add_argument("--stock-type", default="lxr_fc_rights")
    forward.add_argument("--start-date", default="2024-01-01")
    forward.add_argument("--end-date")
    forward.add_argument("--horizons", default="5,20,60")
    forward.set_defaults(func=print_forward_test)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
