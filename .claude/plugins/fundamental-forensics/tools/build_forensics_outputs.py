#!/usr/bin/env python3
"""Build Fundamental Forensics outputs from structured input.

Outputs:
- forensics/red_flag_graph.json
- forensics/fragility_scorecard.json
- forensics/90d_monitor_plan.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class PointSignal:
    name: str
    value: float
    higher_is_riskier: bool
    low: float
    high: float
    weight: float

    def score(self) -> float:
        if self.high <= self.low:
            return 0.0
        if self.higher_is_riskier:
            raw = (self.value - self.low) / (self.high - self.low)
        else:
            raw = (self.low - self.value) / (self.low - self.high)
        return max(0.0, min(100.0, raw * 100.0))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def build_point_signals(payload: dict[str, Any]) -> list[PointSignal]:
    s = payload.get("signals", {})
    return [
        PointSignal("receivables_risk", float(s.get("receivables_to_revenue_pct", 0.0)), True, 15, 45, 1.0),
        PointSignal("ocf_ni_risk", float(s.get("ocf_to_net_income", 1.0)), False, 1.0, 0.4, 1.2),
        PointSignal("inventory_risk", float(s.get("inventory_growth_yoy_pct", 0.0)), True, 10, 40, 0.8),
        PointSignal("goodwill_risk", float(s.get("goodwill_to_equity_pct", 0.0)), True, 20, 60, 0.8),
        PointSignal("pledge_risk", float(s.get("equity_pledge_ratio_pct", 0.0)), True, 5, 35, 1.0),
        PointSignal("insider_risk", float(s.get("insider_net_sell_intensity", 0.0)), True, 0.1, 0.8, 0.7),
        PointSignal("hype_gap_risk", float(s.get("hype_fundamental_gap", 0.0)), True, 20, 80, 0.7),
        PointSignal("st_risk", float(s.get("st_delist_risk_score", 0.0)), True, 15, 75, 1.0),
    ]


def compute_combo_score(point_scores: dict[str, float]) -> tuple[float, list[str]]:
    triggers: list[str] = []
    bonus = 0.0

    if (
        point_scores["receivables_risk"] >= 60
        and point_scores["ocf_ni_risk"] >= 60
        and point_scores["inventory_risk"] >= 50
    ):
        triggers.append("working_capital_deterioration_combo")
        bonus += 8

    if point_scores["pledge_risk"] >= 60 and point_scores["insider_risk"] >= 55:
        triggers.append("governance_liquidity_combo")
        bonus += 7

    if point_scores["goodwill_risk"] >= 55 and point_scores["ocf_ni_risk"] >= 60:
        triggers.append("impairment_pressure_combo")
        bonus += 6

    if point_scores["hype_gap_risk"] >= 60 and point_scores["ocf_ni_risk"] >= 55:
        triggers.append("narrative_reality_combo")
        bonus += 6

    base = sum(point_scores.values()) / max(len(point_scores), 1)
    combo = clamp(base + bonus)
    return combo, triggers


def compute_fragility_score(payload: dict[str, Any]) -> tuple[dict[str, float], float, dict[str, Any]]:
    points = {p.name: round(p.score(), 2) for p in build_point_signals(payload)}
    combo_score, combos = compute_combo_score(points)

    fq = clamp((points["receivables_risk"] + points["ocf_ni_risk"] + points["inventory_risk"]) / 3)
    gv = clamp((points["pledge_risk"] + points["insider_risk"] + points["st_risk"]) / 3)
    bs = clamp((points["goodwill_risk"] + points["ocf_ni_risk"]) / 2)
    tr = clamp((points["hype_gap_risk"] * 0.6 + points["insider_risk"] * 0.4))
    ng = clamp(points["hype_gap_risk"])
    ex = clamp(points["st_risk"])

    weighted = fq * 0.30 + gv * 0.25 + bs * 0.15 + tr * 0.10 + ng * 0.10 + ex * 0.10
    chain_amplifier = max(0.0, combo_score - 50.0) * 0.15
    mitigants = float(payload.get("mitigants", {}).get("credit", 0.0))
    uncertainty_penalty = float(payload.get("data_quality", {}).get("uncertainty_penalty", 0.0))

    fragility = clamp(weighted + chain_amplifier - mitigants + uncertainty_penalty)
    details = {
        "point_scores": points,
        "combo_score": round(combo_score, 2),
        "combo_triggers": combos,
        "subscores": {
            "FQ": round(fq, 2),
            "GV": round(gv, 2),
            "BS": round(bs, 2),
            "TR": round(tr, 2),
            "NG": round(ng, 2),
            "EX": round(ex, 2),
        },
    }
    return points, round(fragility, 2), details


def band(score: float) -> str:
    if score < 25:
        return "Low"
    if score < 50:
        return "Moderate"
    if score < 70:
        return "Elevated"
    if score < 85:
        return "High"
    return "Critical"


def build_red_flag_graph(payload: dict[str, Any], score: float, details: dict[str, Any]) -> dict[str, Any]:
    points = details["point_scores"]
    as_of = payload.get("as_of_date") or date.today().isoformat()

    nodes = [
        {"id": "n_receivables", "type": "EVIDENCE", "label": "应收质量恶化", "score": points["receivables_risk"]},
        {"id": "n_ocf", "type": "EVIDENCE", "label": "现金流与利润背离", "score": points["ocf_ni_risk"]},
        {"id": "n_pledge", "type": "EVIDENCE", "label": "股权质押/治理压力", "score": points["pledge_risk"]},
        {"id": "n_quality", "type": "RISK_STATE", "label": "盈利质量恶化", "score": round((points["receivables_risk"] + points["ocf_ni_risk"]) / 2, 2)},
        {"id": "n_valuation", "type": "IMPACT", "label": "估值压缩风险", "score": score},
    ]

    edges = [
        {"from": "n_receivables", "to": "n_quality", "relation": "supports", "weight": round(points["receivables_risk"] / 100, 2)},
        {"from": "n_ocf", "to": "n_quality", "relation": "supports", "weight": round(points["ocf_ni_risk"] / 100, 2)},
        {"from": "n_quality", "to": "n_valuation", "relation": "amplifies", "weight": round(score / 100, 2)},
        {"from": "n_pledge", "to": "n_valuation", "relation": "amplifies", "weight": round(points["pledge_risk"] / 100, 2)},
    ]

    return {
        "as_of_date": as_of,
        "symbol": payload.get("symbol", "UNKNOWN"),
        "market": payload.get("market", "CN"),
        "nodes": nodes,
        "edges": edges,
        "combo_triggers": details["combo_triggers"],
        "chain_confidence": round(min(0.95, 0.45 + (score / 200)), 2),
        "invalidators": payload.get("invalidators", []),
    }


def build_scorecard(payload: dict[str, Any], score: float, details: dict[str, Any]) -> dict[str, Any]:
    as_of = payload.get("as_of_date") or date.today().isoformat()
    trend = payload.get("trend", {})

    point_sorted = sorted(details["point_scores"].items(), key=lambda x: x[1], reverse=True)
    top = [name for name, _ in point_sorted[:3]]

    return {
        "as_of_date": as_of,
        "symbol": payload.get("symbol", "UNKNOWN"),
        "market": payload.get("market", "CN"),
        "fragility_score": score,
        "band": band(score),
        "subscores": details["subscores"],
        "combo_score": details["combo_score"],
        "combo_triggers": details["combo_triggers"],
        "delta_30d": float(trend.get("delta_30d", 0.0)),
        "delta_90d": float(trend.get("delta_90d", 0.0)),
        "fragility_trend": trend.get("fragility_trend", "unstable"),
        "top_drivers": top,
        "mitigants": payload.get("mitigants", {}),
        "invalidators": payload.get("invalidators", []),
        "confidence": round(max(0.05, 1 - float(payload.get("data_quality", {}).get("missing_ratio", 0.0))), 2),
    }


def build_monitor_plan(payload: dict[str, Any], score: float) -> dict[str, Any]:
    as_of = payload.get("as_of_date") or date.today().isoformat()

    escalation = {
        "yellow": "fragility_score >= 60",
        "orange": "fragility_score >= 70 or delta_30d >= 10",
        "red": "fragility_score >= 85 or ST/delist risk triggered",
    }

    return {
        "as_of_date": as_of,
        "symbol": payload.get("symbol", "UNKNOWN"),
        "monitor_horizon_days": 90,
        "risk_band": band(score),
        "watch_items": [
            {
                "name": "应收周转与账龄结构",
                "frequency": "monthly",
                "trigger": "行业分位 > 80 且连续两期恶化",
                "action": "提升FQ权重并触发盈利质量复核",
            },
            {
                "name": "经营现金流/净利润",
                "frequency": "quarterly",
                "trigger": "< 0.8 且同比下行",
                "action": "上调估值折价情景并刷新red_flag_graph",
            },
            {
                "name": "股权质押与股东行为",
                "frequency": "event-driven",
                "trigger": "新增质押>3pct 或大股东连续减持",
                "action": "触发治理专项预警",
            },
        ],
        "escalation_rules": escalation,
    }


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Fundamental Forensics JSON outputs")
    parser.add_argument("--input", required=True, type=Path, help="Input JSON path")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output root directory")
    args = parser.parse_args()

    payload = load_json(args.input)
    _, score, details = compute_fragility_score(payload)

    out_root = args.output_dir / "forensics"
    dump_json(out_root / "red_flag_graph.json", build_red_flag_graph(payload, score, details))
    dump_json(out_root / "fragility_scorecard.json", build_scorecard(payload, score, details))
    dump_json(out_root / "90d_monitor_plan.json", build_monitor_plan(payload, score))


if __name__ == "__main__":
    main()
