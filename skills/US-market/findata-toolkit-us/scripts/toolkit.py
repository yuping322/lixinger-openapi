#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
import os

# Ensure scripts directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from entities.stock import get_stock_entity
from entities.fund import get_fund_entity
from entities.market import get_market_entity
from entities.sector import get_sector_entity
from entities.macro import get_macro_entity
from common.screener_db import ScreenerDB
from common.lixinger_client import LixingerClient
from legacy.views.registry import discover_views

# 自动发现所有可用技能
ALL_SKILLS = discover_views()

def main():
    parser = argparse.ArgumentParser(description="US Market Toolkit (Lixinger Powered)")
    
    # Entity Commands
    parser.add_argument("--stock", help="Fetch detailed report for a stock code (e.g., 600519)")
    parser.add_argument("--fund", help="Fetch detailed report for a fund code (e.g., 510300)")
    parser.add_argument("--market", action="store_true", help="Fetch market overview")
    parser.add_argument("--sector", help="Fetch sector/industry detail by code")
    parser.add_argument("--macro", action="store_true", help="Fetch macro economic pulse")
    
    # Mode/Options
    parser.add_argument("--mode", choices=["brief", "full"], default="brief", help="Level of detail (default: brief)")
    
    # Discovery/Screening
    parser.add_argument("--screen", help="Perform SQL-style screening (e.g., 'pe_ttm < 20 AND industry=\"白酒\"')")
    parser.add_argument("--sync", action="store_true", help="Sync local screener database from Lixinger")
    
    # Skill Execution
    parser.add_argument("--skill", help=f"Run specific skill. Available skills: {', '.join(ALL_SKILLS.keys())}")
    parser.add_argument("--skill-params", help="JSON string of parameters for the skill")

    # Raw Query Fallback
    parser.add_argument("--raw", help="Directly query Lixinger API suffix (e.g., 'cn/company/block-trade')")
    parser.add_argument("--params", help="JSON string for raw query parameters")

    args = parser.parse_args()

    # Execution Routing
    try:
        if args.stock:
            result = get_stock_entity(args.stock, mode=args.mode)
        elif args.fund:
            result = get_fund_entity(args.fund)
        elif args.market:
            result = get_market_entity()
        elif args.sector:
            result = get_sector_entity(args.sector)
        elif args.macro:
            result = get_macro_entity()
        elif args.screen:
            db = ScreenerDB()
            result = db.query(args.screen)
        elif args.sync:
            client = LixingerClient()
            db = ScreenerDB()
            if db.sync_from_lixinger(client):
                result = {"status": "success", "message": "Screener DB synced."}
            else:
                result = {"status": "error", "message": "Sync failed."}
        elif args.skill:
            if args.skill not in ALL_SKILLS:
                result = {"error": f"Skill {args.skill} not found. Available skills: {', '.join(ALL_SKILLS.keys())}"}
            else:
                skill = ALL_SKILLS[args.skill]
                params = json.loads(args.skill_params) if args.skill_params else {}
                result = skill.module.plan(params)
        elif args.raw:
            client = LixingerClient()
            params = json.loads(args.params) if args.params else {}
            result = client.fetch(args.raw, params)
        else:
            parser.print_help()
            sys.exit(0)

        # Unified Output
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
