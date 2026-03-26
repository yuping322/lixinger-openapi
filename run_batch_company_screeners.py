#!/usr/bin/env python3
"""
分批或一次性运行 company-fundamental 筛选器。

默认会跳过：
1. 已成功拉取的筛选器
2. 已经失败过的筛选器

这样不会因为前几个坏筛选器一直重试而卡住后面的 900+ 条数据。
如需重新尝试失败项，请传 --retry-errors。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from glob import glob
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_LINKS_FILE = ROOT / "links.txt"
DEFAULT_SKILL_DIR = ROOT / ".claude" / "skills" / "lixinger-screener"
DEFAULT_OUTPUT_DIR = ROOT / "url_results"

SCREENER_ID_RE = re.compile(r"screener-id=([a-zA-Z0-9]+)")


def extract_screener_id(text: str | None) -> str | None:
    if not text:
        return None
    match = SCREENER_ID_RE.search(text)
    return match.group(1) if match else None


def classify_error_text(error_text: str) -> str:
    lowered = error_text.lower()
    if "validationerror" in lowered or "request failed 400" in lowered:
        return "permanent"
    if "request failed 401" in lowered:
        return "permanent"
    if "request failed 429" in lowered:
        return "transient"
    if "request failed 502" in lowered:
        return "transient"
    if "timeout" in lowered or "fetch failed" in lowered or "econnreset" in lowered:
        return "transient"
    return "unknown"


def extract_all_company_fundamental_urls(file_path: Path) -> list[dict[str, str]]:
    urls: list[dict[str, str]] = []
    seen: set[str] = set()

    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            url = data.get("url", "")
            if "company-fundamental/" not in url or "screener-id=" not in url:
                continue

            screener_id = extract_screener_id(url)
            if not screener_id or screener_id in seen:
                continue
            seen.add(screener_id)

            area = "cn"
            if "/hk" in url:
                area = "hk"
            elif "/us" in url:
                area = "us"

            urls.append(
                {
                    "url": url,
                    "screener_id": screener_id,
                    "area": area,
                }
            )

    return urls


def read_success_ids(output_dir: Path) -> set[str]:
    success_ids: set[str] = set()
    for filepath in glob(str(output_dir / "screener_*.json")):
        path = Path(filepath)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = None

        if isinstance(data, dict):
            screener_id = data.get("screenerId")
            if isinstance(screener_id, str) and screener_id:
                success_ids.add(screener_id)
                continue

        match = re.search(r"screener_[a-z]+_([a-f0-9]+)\.json$", path.name)
        if match:
            success_ids.add(match.group(1))

    return success_ids


def read_error_states(output_dir: Path) -> dict[str, str]:
    error_states: dict[str, str] = {}
    for filepath in glob(str(output_dir / "screener_*_error.txt")):
        path = Path(filepath)
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            content = ""

        screener_id = extract_screener_id(content)
        if not screener_id:
            match = re.search(r"screener_[a-z]+_([a-f0-9]+)_error\.txt$", path.name)
            screener_id = match.group(1) if match else None
        if not screener_id:
            continue

        error_states[screener_id] = classify_error_text(content)

    return error_states


def run_fetch(skill_dir: Path, url: str, output_format: str, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    cmd = [
        "node",
        "request/fetch-lixinger-screener.js",
        "--url",
        url,
        "--output",
        output_format,
    ]
    return subprocess.run(
        cmd,
        cwd=skill_dir,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )


def run_screener(
    url_info: dict[str, str],
    output_dir: Path,
    skill_dir: Path,
    timeout_seconds: int,
    max_retries: int,
) -> dict[str, Any]:
    screener_id = url_info["screener_id"]
    url = url_info["url"]
    area = url_info["area"]

    json_file = output_dir / f"screener_{area}_{screener_id}.json"
    md_file = output_dir / f"screener_{area}_{screener_id}.md"
    error_file = output_dir / f"screener_{area}_{screener_id}_error.txt"

    last_error = ""
    for attempt in range(1, max_retries + 2):
        try:
            result = run_fetch(skill_dir, url, "table-json", timeout_seconds)
            if result.returncode != 0:
                last_error = result.stderr.strip() or result.stdout.strip() or f"Exit code {result.returncode}"
                if classify_error_text(last_error) == "transient" and attempt <= max_retries:
                    time.sleep(attempt * 2)
                    continue
                break

            json_file.write_text(result.stdout, encoding="utf-8")

            result_md = run_fetch(skill_dir, url, "markdown", timeout_seconds)
            if result_md.returncode == 0:
                md_file.write_text(result_md.stdout, encoding="utf-8")

            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                data = {}

            return {
                "success": True,
                "attempts": attempt,
                "screener_id": screener_id,
                "area": area,
                "total": data.get("total", 0),
                "screener_name": data.get("screenerName", "Unknown"),
                "screener_description": data.get("screenerDescription"),
                "json_file": json_file.name,
                "md_file": md_file.name,
            }

        except subprocess.TimeoutExpired:
            last_error = "Timeout"
            if attempt <= max_retries:
                time.sleep(attempt * 2)
                continue
            break
        except Exception as exc:
            last_error = str(exc)
            break

    error_file.write_text(f"URL: {url}\nError: {last_error}\n", encoding="utf-8")
    return {
        "success": False,
        "attempts": max_retries + 1,
        "screener_id": screener_id,
        "area": area,
        "error": last_error[:300],
        "error_type": classify_error_text(last_error),
        "error_file": error_file.name,
    }


def save_batch_summary(output_dir: Path, results: list[dict[str, Any]], meta: dict[str, Any]) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"_summary_batch_{timestamp}.json"
    md_path = output_dir / f"_summary_batch_{timestamp}.md"

    payload = {
        "timestamp": datetime.now().isoformat(),
        "meta": meta,
        "results": results,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    success_count = sum(1 for item in results if item.get("success"))
    fail_count = len(results) - success_count
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Company Fundamental Screener 批次结果\n\n")
        handle.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        handle.write(f"总计: {len(results)} | 成功: {success_count} | 失败: {fail_count}\n\n")
        handle.write("| # | 区域 | Screener ID | 名称 | 结果数 | 状态 |\n")
        handle.write("|---|------|-------------|------|--------|------|\n")
        for index, item in enumerate(results, 1):
            name = (item.get("screener_name") or "N/A")[:25]
            total = item.get("total", "N/A") if item.get("success") else "N/A"
            status = "success" if item.get("success") else item.get("error_type", "failed")
            handle.write(
                f"| {index} | {item.get('area', 'N/A')} | {item['screener_id'][:16]}... | "
                f"{name} | {total} | {status} |\n"
            )


def build_todo_list(
    all_urls: list[dict[str, str]],
    success_ids: set[str],
    error_states: dict[str, str],
    retry_errors: bool,
) -> list[dict[str, str]]:
    if retry_errors:
        return [item for item in all_urls if item["screener_id"] not in success_ids]

    done_ids = success_ids | set(error_states.keys())
    return [item for item in all_urls if item["screener_id"] not in done_ids]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Lixinger company-fundamental screeners in batches.")
    parser.add_argument("--links-file", default=str(DEFAULT_LINKS_FILE))
    parser.add_argument("--skill-dir", default=str(DEFAULT_SKILL_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--batch-size", type=int, default=50, help="How many new screeners to process.")
    parser.add_argument("--all", action="store_true", help="Process every remaining screener in one run.")
    parser.add_argument("--retry-errors", action="store_true", help="Retry previously failed screeners too.")
    parser.add_argument("--max-retries", type=int, default=1, help="Retries for transient failures.")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per fetch call in seconds.")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers for network fetches.")
    parser.add_argument("--area", choices=["cn", "hk", "us", "all"], default="all")
    return parser.parse_args()


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    args = parse_args()

    links_file = Path(args.links_file)
    skill_dir = Path(args.skill_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_urls = extract_all_company_fundamental_urls(links_file)
    if args.area != "all":
        all_urls = [item for item in all_urls if item["area"] == args.area]

    success_ids = read_success_ids(output_dir)
    error_states = read_error_states(output_dir)
    todo_urls = build_todo_list(all_urls, success_ids, error_states, retry_errors=args.retry_errors)

    print(f"总筛选器: {len(all_urls)}")
    print(f"已成功: {len(success_ids)}")
    print(f"已失败: {len(error_states)} | 分类: {dict(Counter(error_states.values()))}")
    print(f"待处理: {len(todo_urls)}")

    if not todo_urls:
        print("\n✓ 没有剩余任务。")
        return 0

    batch = todo_urls if args.all else todo_urls[: args.batch_size]
    print(f"\n本次将处理: {len(batch)}")
    print(f"剩余未处理: {len(todo_urls) - len(batch)}")
    print("=" * 72)

    results: list[dict[str, Any]] = []
    success_count = 0
    failed_count = 0

    if args.workers <= 1:
        for index, url_info in enumerate(batch, 1):
            prefix = f"[{index}/{len(batch)}] {url_info['screener_id'][:20]}... [{url_info['area']}]"
            print(prefix, end=" ")
            result = run_screener(
                url_info=url_info,
                output_dir=output_dir,
                skill_dir=skill_dir,
                timeout_seconds=args.timeout,
                max_retries=args.max_retries,
            )
            results.append(result)

            if result["success"]:
                success_count += 1
                total = result.get("total", 0)
                name = (result.get("screener_name") or "N/A")[:30]
                attempts = result.get("attempts", 1)
                print(f"✓ {total:4d} | attempts={attempts} | {name}")
            else:
                failed_count += 1
                attempts = result.get("attempts", 1)
                error_type = result.get("error_type", "unknown")
                print(f"✗ {error_type} | attempts={attempts} | {result.get('error', 'Unknown')[:60]}")
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_index = {
                executor.submit(
                    run_screener,
                    url_info=url_info,
                    output_dir=output_dir,
                    skill_dir=skill_dir,
                    timeout_seconds=args.timeout,
                    max_retries=args.max_retries,
                ): (index, url_info)
                for index, url_info in enumerate(batch, 1)
            }

            for future in concurrent.futures.as_completed(future_to_index):
                index, url_info = future_to_index[future]
                result = future.result()
                results.append(result)
                prefix = f"[{index}/{len(batch)}] {url_info['screener_id'][:20]}... [{url_info['area']}]"

                if result["success"]:
                    success_count += 1
                    total = result.get("total", 0)
                    name = (result.get("screener_name") or "N/A")[:30]
                    attempts = result.get("attempts", 1)
                    print(f"{prefix} ✓ {total:4d} | attempts={attempts} | {name}")
                else:
                    failed_count += 1
                    attempts = result.get("attempts", 1)
                    error_type = result.get("error_type", "unknown")
                    print(
                        f"{prefix} ✗ {error_type} | attempts={attempts} | "
                        f"{result.get('error', 'Unknown')[:60]}"
                    )

    save_batch_summary(
        output_dir=output_dir,
        results=results,
        meta={
            "total_urls": len(all_urls),
            "batch_size": len(batch),
            "retry_errors": args.retry_errors,
            "timeout": args.timeout,
            "max_retries": args.max_retries,
            "success_seen_before_run": len(success_ids),
            "error_seen_before_run": len(error_states),
        },
    )

    print("\n" + "=" * 72)
    print("本次完成")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"下一次剩余: {len(todo_urls) - len(batch)}")
    if not args.all and len(todo_urls) - len(batch) > 0:
        print("提示: 继续执行同一命令即可接着跑后面的，不会被旧错误卡住。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
