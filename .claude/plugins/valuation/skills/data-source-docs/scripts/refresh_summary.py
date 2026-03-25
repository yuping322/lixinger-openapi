#!/usr/bin/env python3
"""Refresh or read provider summaries.

This script is intentionally lightweight and does not attempt full parsing.
It stores a minimal summary object that other modules can consume.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional


CACHE_DIR = Path("docs/data-sources/cache")


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _is_fresh(path: Path, ttl_days: int) -> bool:
    if not path.exists():
        return False
    mtime = dt.datetime.fromtimestamp(path.stat().st_mtime)
    return (dt.datetime.now() - mtime).days <= ttl_days


def _guess_base_url(text: str) -> Optional[str]:
    # Very conservative: pick the first https URL that looks like an API base.
    match = re.search(r"https://[a-zA-Z0-9./_-]*api[./_-][a-zA-Z0-9./_-]*", text)
    return match.group(0) if match else None


def _build_stub(provider: str, source: str, notes: str) -> Dict:
    return {
        "provider": provider,
        "base_url": None,
        "auth": {"type": "unknown", "location": None, "name": None},
        "endpoints": [],
        "rate_limit": "unknown",
        "last_updated": dt.date.today().isoformat(),
        "source": source,
        "notes": notes,
    }


def _summarize(provider: str, text: str, source: str) -> Dict:
    base_url = _guess_base_url(text)
    summary = _build_stub(provider, source, "Summary generated from provider docs.")
    if base_url:
        summary["base_url"] = base_url
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh provider summary cache")
    parser.add_argument("--provider", required=True, help="provider key")
    parser.add_argument("--doc-file", help="local saved doc file path")
    parser.add_argument("--force", action="store_true", help="force refresh")
    parser.add_argument("--ttl-days", type=int, default=30, help="cache TTL in days")
    args = parser.parse_args()

    provider = args.provider.strip().lower()
    cache_path = CACHE_DIR / f"{provider}.json"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not args.force and _is_fresh(cache_path, args.ttl_days):
        print(_read_file(cache_path))
        return 0

    text = None
    source = "cache"

    if args.doc_file:
        path = Path(args.doc_file)
        if not path.exists():
            print(f"Doc file not found: {path}", file=sys.stderr)
            return 1
        text = _read_file(path)
        source = "doc_file"
    if text is None:
        summary = _build_stub(provider, "cache", "No doc file provided.")
    else:
        summary = _summarize(provider, text, source)

    cache_path.write_text(json.dumps(summary, ensure_ascii=True), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
