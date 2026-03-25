#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _safe_div(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b is None:
        return None
    if b == 0:
        return None
    return a / b


def _pct_change(curr: Optional[float], prev: Optional[float]) -> Optional[float]:
    if curr is None or prev is None:
        return None
    if prev == 0:
        return None
    return (curr - prev) / prev


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _score_from_ratio(r: Optional[float], good: Tuple[float, float], bad: Tuple[float, float]) -> float:
    """Map a ratio to [0,1]. good/bad are (low, high) anchors."""
    if r is None or math.isnan(r):
        return 0.5
    if r >= good[1]:
        return 1.0
    if r <= bad[0]:
        return 0.0
    return _clamp((r - bad[0]) / (good[1] - bad[0]), 0.0, 1.0)


@dataclass
class RedFlag:
    id: str
    severity: str
    category: str
    title: str
    description: str
    rule_id: str
    evidence_refs: List[str]
    possible_explanations: List[str]
    status: str = "open"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "rule_id": self.rule_id,
            "evidence_refs": self.evidence_refs,
            "possible_explanations": self.possible_explanations,
            "status": self.status,
        }


@dataclass
class EvidenceItem:
    id: str
    source: str
    as_of_date: str
    confidence: float
    notes: str
    payload: Dict[str, Any]

    def to_jsonl(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "source": self.source,
                "as_of_date": self.as_of_date,
                "confidence": self.confidence,
                "notes": self.notes,
                "payload": self.payload,
            },
            ensure_ascii=False,
        )


def _load_rules(rules_path: Optional[Path]) -> Dict[str, Any]:
    if rules_path is None or not rules_path.exists():
        return {}
    payload = json.loads(rules_path.read_text(encoding="utf-8"))
    return payload.get("rules") or {}


def _rule_num(rules: Dict[str, Any], rule_id: str, path: List[str], default: Optional[float]) -> Optional[float]:
    cur: Any = rules.get(rule_id)
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    if cur is None:
        return default
    try:
        return float(cur)
    except Exception:
        return default


def _latest_period(periods: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not periods:
        raise ValueError("periods is empty")
    return periods[-1]


def _build_adjustments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    adjs = []
    for item in payload.get("one_off_adjustments", []) or []:
        adjs.append(
            {
                "id": item.get("id") or "adj_manual",
                "period": item.get("period") or (payload.get("periods") or [{}])[-1].get("period") or "",
                "category": item.get("category") or "manual",
                "sub_category": item.get("sub_category") or "",
                "direction": item.get("direction") or "subtract",
                "amount": item.get("amount") or 0,
                "currency": payload.get("currency", ""),
                "unit": payload.get("unit", ""),
                "impact_area": item.get("impact_area") or "net_income",
                "reason": item.get("reason") or "",
                "source_refs": item.get("source_refs") or [],
                "confidence": item.get("confidence") if item.get("confidence") is not None else 0.6,
            }
        )
    return adjs


def _apply_adjustments_to_net_income(reported_ni: float, adjustments: List[Dict[str, Any]]) -> float:
    adjusted = reported_ni
    for a in adjustments:
        direction = a.get("direction")
        amt = float(a.get("amount") or 0)
        if direction == "subtract":
            adjusted -= amt
        elif direction == "add":
            adjusted += amt
    return adjusted


# ---------------------------------------------------------------------------
# Trend helpers
# ---------------------------------------------------------------------------

def _ocf_ni_series(periods: List[Dict[str, Any]]) -> List[Optional[float]]:
    """Return OCF/NI ratio for each period (None if not computable)."""
    return [_safe_div(p.get("operating_cash_flow"), p.get("net_income")) for p in periods]


def _count_below_in_window(series: List[Optional[float]], threshold: float, tail: int) -> int:
    """Count how many of the last `tail` values are below threshold (skip None)."""
    window = [v for v in series[-tail:] if v is not None]
    return sum(1 for v in window if v < threshold)


def _latest_run_length_below(series: List[Optional[float]], threshold: float) -> int:
    """Count the length of the trailing run of values below threshold (skip None)."""
    run = 0
    for v in reversed(series):
        if v is None:
            continue
        if v < threshold:
            run += 1
        else:
            break
    return run


def _compute_red_flags(payload: Dict[str, Any], rules: Dict[str, Any]) -> List["RedFlag"]:
    periods = payload.get("periods") or []
    if len(periods) < 2:
        return []

    latest = periods[-1]
    prev = periods[-2]
    latest_period = latest.get("period", "latest")

    # Core metrics (latest period)
    rev = latest.get("revenue")
    rev_prev = prev.get("revenue")
    ni = latest.get("net_income")
    ocf = latest.get("operating_cash_flow")
    capex = latest.get("capex")
    ar = latest.get("accounts_receivable")
    ar_prev = prev.get("accounts_receivable")
    inv = latest.get("inventory")
    inv_prev = prev.get("inventory")
    goodwill = latest.get("goodwill")
    equity = latest.get("equity")
    cash = latest.get("cash")
    st_debt = latest.get("short_term_debt")
    total_debt = latest.get("total_debt")

    rev_yoy = _pct_change(rev, rev_prev)
    ar_yoy = _pct_change(ar, ar_prev)
    inv_yoy = _pct_change(inv, inv_prev)

    ocf_to_ni = _safe_div(ocf, ni)
    fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
    fcf_to_ni = _safe_div(fcf, ni)

    goodwill_to_equity = _safe_div(goodwill, equity)
    st_debt_to_cash = _safe_div(st_debt, cash)
    net_debt = (total_debt - cash) if (total_debt is not None and cash is not None) else None
    net_debt_to_equity = _safe_div(net_debt, equity)

    flags: List[RedFlag] = []

    # ------------------------------------------------------------------
    # fq_cash_003: OCF/NI low (single period)
    # ------------------------------------------------------------------
    ocf_med = _rule_num(rules, "fq_cash_003", ["severity", "medium", "ocf_to_ni_lt"], 0.8)
    ocf_high = _rule_num(rules, "fq_cash_003", ["severity", "high", "ocf_to_ni_lt"], 0.5)
    if ocf_to_ni is not None and ocf_med is not None and ocf_to_ni < ocf_med:
        flags.append(
            RedFlag(
                id=f"flag_ocf_support_{latest_period}",
                severity="high" if (ocf_high is not None and ocf_to_ni < ocf_high) else "medium",
                category="cash_quality",
                title="经营现金流无法支撑报告净利润",
                description=f"{latest_period} OCF/NI={ocf_to_ni:.2f}，低于 {ocf_med:.2f}",
                rule_id="fq_cash_003",
                evidence_refs=[f"operating_cash_flow:{latest_period}", f"net_income:{latest_period}"],
                possible_explanations=["营运资本占用上升", "收入确认与回款错配", "一次性利润或应计偏高"],
            )
        )

    # ------------------------------------------------------------------
    # fq_cash_003t: OCF/NI 连续 N 期偏低（真正的连续 run，不是计数）
    # min_run: 触发所需的最短连续期数
    # ------------------------------------------------------------------
    trend_min_run = int(_rule_num(rules, "fq_cash_003t", ["params", "min_run"], 2) or 2)
    trend_threshold = _rule_num(rules, "fq_cash_003t", ["params", "ocf_to_ni_lt"], 0.85)
    if trend_threshold is not None and len(periods) >= trend_min_run:
        ocf_ni_series = _ocf_ni_series(periods)
        run_len = _latest_run_length_below(ocf_ni_series, trend_threshold)
        if run_len >= trend_min_run:
            run_periods = periods[-run_len:]
            period_labels = [p.get("period", "?") for p in run_periods]
            flags.append(
                RedFlag(
                    id=f"flag_ocf_trend_{latest_period}",
                    severity="high",
                    category="cash_quality",
                    title=f"OCF/NI 连续 {run_len} 期低于 {trend_threshold:.0%}（持续恶化）",
                    description=f"连续 {run_len} 期（{', '.join(period_labels)}）OCF/NI 均 < {trend_threshold:.2f}",
                    rule_id="fq_cash_003t",
                    evidence_refs=[f"operating_cash_flow:{p.get('period', '?')}" for p in run_periods]
                               + [f"net_income:{p.get('period', '?')}" for p in run_periods],
                    possible_explanations=["盈利质量系统性下滑", "应计利润持续累积", "营运资本管理恶化"],
                )
            )

    # ------------------------------------------------------------------
    # fq_cash_005: FCF/NI low
    # ------------------------------------------------------------------
    fcf_med = _rule_num(rules, "fq_cash_005", ["severity", "medium", "fcf_to_ni_lt"], 0.6)
    fcf_high = _rule_num(rules, "fq_cash_005", ["severity", "high", "fcf_to_ni_lt"], 0.3)
    if fcf_to_ni is not None and fcf_med is not None and fcf_to_ni < fcf_med:
        flags.append(
            RedFlag(
                id=f"flag_fcf_support_{latest_period}",
                severity="high" if (fcf_high is not None and fcf_to_ni < fcf_high) else "medium",
                category="cash_quality",
                title="自由现金流覆盖不足",
                description=f"{latest_period} FCF/NI={fcf_to_ni:.2f}，低于 {fcf_med:.2f}（FCF=OCF-Capex）",
                rule_id="fq_cash_005",
                evidence_refs=[f"operating_cash_flow:{latest_period}", f"capex:{latest_period}", f"net_income:{latest_period}"],
                possible_explanations=["高资本开支阶段", "营运资本拖累", "利润质量偏弱"],
            )
        )

    # ------------------------------------------------------------------
    # fq_rev_001: AR growth >> revenue growth
    # ------------------------------------------------------------------
    ar_med = _rule_num(rules, "fq_rev_001", ["params", "delta_yoy_gt", "medium"], 0.20)
    ar_high = _rule_num(rules, "fq_rev_001", ["params", "delta_yoy_gt", "high"], 0.35)
    if ar_yoy is not None and rev_yoy is not None and ar_med is not None and (ar_yoy - rev_yoy) > ar_med:
        flags.append(
            RedFlag(
                id=f"flag_ar_vs_rev_{latest_period}",
                severity="high" if (ar_high is not None and (ar_yoy - rev_yoy) > ar_high) else "medium",
                category="revenue_quality",
                title="应收增速显著快于收入增速",
                description=f"{latest_period} AR YoY={ar_yoy:.1%}，Revenue YoY={rev_yoy:.1%}，差值={ar_yoy - rev_yoy:.1%}",
                rule_id="fq_rev_001",
                evidence_refs=[f"accounts_receivable:{latest_period}", f"revenue:{latest_period}"],
                possible_explanations=["渠道压货", "账期拉长", "回款风险上升", "确认节奏前置"],
            )
        )

    # ------------------------------------------------------------------
    # fq_rev_001t: AR/Revenue 比率连续上升（trailing run，语义对齐）
    # min_run: 触发所需的最短连续上升期数
    # ------------------------------------------------------------------
    ar_rev_min_run = int(_rule_num(rules, "fq_rev_001t", ["params", "min_run"], 2) or 2)
    if len(periods) >= ar_rev_min_run + 1:
        # 需要 n+1 个点才能算 n 个变化方向
        ar_rev_ratios = [_safe_div(p.get("accounts_receivable"), p.get("revenue")) for p in periods]
        # 计算 trailing run of rising
        run = 0
        for i in range(len(ar_rev_ratios) - 1, 0, -1):
            curr, prev_r = ar_rev_ratios[i], ar_rev_ratios[i - 1]
            if curr is None or prev_r is None:
                break
            if curr > prev_r:
                run += 1
            else:
                break
        if run >= ar_rev_min_run:
            run_periods = periods[-(run + 1):]  # +1 因为 run 个变化需要 run+1 个点
            period_labels = [p.get("period", "?") for p in run_periods]
            flags.append(
                RedFlag(
                    id=f"flag_ar_rev_trend_{latest_period}",
                    severity="medium",
                    category="revenue_quality",
                    title=f"应收/收入比率连续 {run} 期上升（持续恶化）",
                    description=f"连续 {run} 期（{', '.join(period_labels[1:])}）应收占收入比逐期扩大",
                    rule_id="fq_rev_001t",
                    evidence_refs=[f"accounts_receivable:{p.get('period', '?')}" for p in run_periods[1:]]
                               + [f"revenue:{p.get('period', '?')}" for p in run_periods[1:]],
                    possible_explanations=["回款周期系统性拉长", "收入质量下降", "客户信用风险累积"],
                )
            )

    # ------------------------------------------------------------------
    # fq_bs_002: inventory growth >> revenue growth
    # ------------------------------------------------------------------
    inv_med = _rule_num(rules, "fq_bs_002", ["params", "delta_yoy_gt", "medium"], 0.20)
    inv_high = _rule_num(rules, "fq_bs_002", ["params", "delta_yoy_gt", "high"], 0.35)
    if inv_yoy is not None and rev_yoy is not None and inv_med is not None and (inv_yoy - rev_yoy) > inv_med:
        flags.append(
            RedFlag(
                id=f"flag_inv_vs_rev_{latest_period}",
                severity="high" if (inv_high is not None and (inv_yoy - rev_yoy) > inv_high) else "medium",
                category="balance_sheet_quality",
                title="存货增长显著快于收入增长",
                description=f"{latest_period} Inventory YoY={inv_yoy:.1%}，Revenue YoY={rev_yoy:.1%}，差值={inv_yoy - rev_yoy:.1%}",
                rule_id="fq_bs_002",
                evidence_refs=[f"inventory:{latest_period}", f"revenue:{latest_period}"],
                possible_explanations=["需求不及预期导致积压", "扩产备货", "跌价计提滞后"],
            )
        )

    # ------------------------------------------------------------------
    # fq_bs_004: goodwill / equity high
    # ------------------------------------------------------------------
    gw_med = _rule_num(rules, "fq_bs_004", ["params", "goodwill_to_equity_gt", "medium"], 0.30)
    gw_high = _rule_num(rules, "fq_bs_004", ["params", "goodwill_to_equity_gt", "high"], 0.50)
    if goodwill_to_equity is not None and gw_med is not None and goodwill_to_equity > gw_med:
        flags.append(
            RedFlag(
                id=f"flag_goodwill_{latest_period}",
                severity="high" if (gw_high is not None and goodwill_to_equity > gw_high) else "medium",
                category="balance_sheet_quality",
                title="商誉占净资产比例偏高",
                description=f"{latest_period} Goodwill/Equity={goodwill_to_equity:.1%}",
                rule_id="fq_bs_004",
                evidence_refs=[f"goodwill:{latest_period}", f"equity:{latest_period}"],
                possible_explanations=["并购扩张导致商誉累积", "被并购资产盈利不达预期引发减值风险"],
            )
        )

    # ------------------------------------------------------------------
    # fq_debt_001: short-term debt pressure vs cash
    # ------------------------------------------------------------------
    st_med = _rule_num(rules, "fq_debt_001", ["params", "st_debt_to_cash_gt", "medium"], 0.80)
    st_high = _rule_num(rules, "fq_debt_001", ["params", "st_debt_to_cash_gt", "high"], 1.20)
    if st_debt_to_cash is not None and st_med is not None and st_debt_to_cash > st_med:
        flags.append(
            RedFlag(
                id=f"flag_st_debt_cash_{latest_period}",
                severity="high" if (st_high is not None and st_debt_to_cash > st_high) else "medium",
                category="liability_structure",
                title="短债对现金压力偏高",
                description=f"{latest_period} ShortDebt/Cash={st_debt_to_cash:.2f}",
                rule_id="fq_debt_001",
                evidence_refs=[f"short_term_debt:{latest_period}", f"cash:{latest_period}"],
                possible_explanations=["短期再融资依赖", "经营现金流波动", "债务期限结构不合理"],
            )
        )

    # ------------------------------------------------------------------
    # fq_leverage_002: net debt / equity high
    # ------------------------------------------------------------------
    nd_med = _rule_num(rules, "fq_leverage_002", ["params", "net_debt_to_equity_gt", "medium"], 0.60)
    nd_high = _rule_num(rules, "fq_leverage_002", ["params", "net_debt_to_equity_gt", "high"], 1.00)
    if net_debt_to_equity is not None and nd_med is not None and net_debt_to_equity > nd_med:
        flags.append(
            RedFlag(
                id=f"flag_net_debt_equity_{latest_period}",
                severity="high" if (nd_high is not None and net_debt_to_equity > nd_high) else "medium",
                category="liability_structure",
                title="净负债占净资产比例偏高",
                description=f"{latest_period} NetDebt/Equity={net_debt_to_equity:.1%}",
                rule_id="fq_leverage_002",
                evidence_refs=[f"total_debt:{latest_period}", f"cash:{latest_period}", f"equity:{latest_period}"],
                possible_explanations=["资产负债表杠杆偏高", "利率上行敏感", "盈利下行时抗压能力下降"],
            )
        )

    # ------------------------------------------------------------------
    # Governance overlay
    # ------------------------------------------------------------------
    gov = payload.get("governance") or {}
    if gov.get("audit_opinion") not in (None, "", "unqualified"):
        flags.append(
            RedFlag(
                id=f"flag_audit_opinion_{latest_period}",
                severity="high",
                category="governance_quality",
                title="审计意见非标准",
                description=f"{latest_period} audit_opinion={gov.get('audit_opinion')}",
                rule_id="fq_gov_001",
                evidence_refs=["governance:audit_opinion"],
                possible_explanations=["会计处理存在重大不确定性", "持续经营或内控风险"],
            )
        )
    if gov.get("restatement_in_last_5y") is True:
        flags.append(
            RedFlag(
                id=f"flag_restatement_{latest_period}",
                severity="high",
                category="governance_quality",
                title="近 5 年存在财务重述",
                description="restatement_in_last_5y=true",
                rule_id="fq_gov_002",
                evidence_refs=["governance:restatement_in_last_5y"],
                possible_explanations=["会计差错更正", "收入确认/成本结转口径调整", "历史数据可比性下降"],
            )
        )
    if gov.get("regulatory_inquiry_in_last_3y") is True:
        flags.append(
            RedFlag(
                id=f"flag_reg_inquiry_{latest_period}",
                severity="medium",
                category="governance_quality",
                title="近 3 年存在监管问询/关注函",
                description="regulatory_inquiry_in_last_3y=true",
                rule_id="fq_gov_003",
                evidence_refs=["governance:regulatory_inquiry_in_last_3y"],
                possible_explanations=["信息披露质量需核查", "交易真实性或会计处理被关注"],
            )
        )

    return flags


def _build_min_evidence(payload: Dict[str, Any], red_flags: List[RedFlag]) -> List[EvidenceItem]:
    company = payload.get("company", "")
    as_of_date = payload.get("as_of_date", "")
    source = payload.get("source") or "user_provided_or_sample"

    evidence: List[EvidenceItem] = []
    evidence.append(
        EvidenceItem(
            id=f"evi_financial_facts_{company}_{as_of_date}",
            source=source,
            as_of_date=as_of_date,
            confidence=0.75,
            notes="结构化财务事实（MVP），用于红旗与评分计算",
            payload={"company": company, "period_count": len(payload.get("periods") or [])},
        )
    )

    seen = set()
    for rf in red_flags:
        for ref in rf.evidence_refs:
            if isinstance(ref, str) and ref.startswith("evi_"):
                evi_id = ref
                ref_payload: Dict[str, Any] = {"ref": ref}
            else:
                evi_id = f"evi_metric_{company}_{as_of_date}_{ref}".replace(":", "_")
                ref_payload = {"ref": ref}
            if evi_id in seen:
                continue
            seen.add(evi_id)
            evidence.append(
                EvidenceItem(
                    id=evi_id,
                    source=source,
                    as_of_date=as_of_date,
                    confidence=0.6,
                    notes="指标级证据占位（MVP）：后续可映射到具体报表行/附注/公告来源",
                    payload=ref_payload,
                )
            )
    return evidence


def _evidence_id(company: str, as_of_date: str, ref: str) -> str:
    return f"evi_metric_{company}_{as_of_date}_{ref}".replace(":", "_")


def _rewrite_red_flag_refs_to_evidence_ids(payload: Dict[str, Any], red_flags: List[RedFlag]) -> None:
    company = payload.get("company", "")
    as_of_date = payload.get("as_of_date", "")
    for rf in red_flags:
        rf.evidence_refs = [_evidence_id(company, as_of_date, r) for r in rf.evidence_refs]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _compute_accrual_quality(periods: List[Dict[str, Any]]) -> float:
    """
    应计质量（Accrual Quality）：基于 Sloan (1996) 思路的简化版。
    公式：accrual_ratio = (NI - OCF) / avg_total_assets
    - 优先用 total_assets；若缺失则 fallback 到 equity（需在 notes 中标注）
    - 应计比率越低（甚至为负）越好：OCF > NI 说明利润有现金支撑
    - 返回 [0,1]，1 = 应计比率低（质量好）
    """
    if len(periods) < 2:
        return 0.5  # 数据不足，中性

    accrual_ratios = []
    for i in range(1, len(periods)):
        p = periods[i]
        p_prev = periods[i - 1]
        ni = p.get("net_income")
        ocf = p.get("operating_cash_flow")
        # 优先 total_assets，fallback equity
        assets = p.get("total_assets")
        assets_prev = p_prev.get("total_assets")
        if assets is None or assets_prev is None:
            assets = p.get("equity")
            assets_prev = p_prev.get("equity")
        if ni is None or ocf is None or assets is None or assets_prev is None:
            continue
        avg_assets = (assets + assets_prev) / 2
        if avg_assets == 0:
            continue
        accrual_ratio = (ni - ocf) / avg_assets
        accrual_ratios.append(accrual_ratio)

    if not accrual_ratios:
        return 0.5

    avg_accrual = sum(accrual_ratios) / len(accrual_ratios)
    # 应计比率越低越好：
    #   avg_accrual <= -0.02 → score=1.0（OCF 显著超过 NI，现金质量好）
    #   avg_accrual == 0     → score≈0.67（中性）
    #   avg_accrual >= 0.08  → score=0.0（NI 显著超过 OCF，应计堆积）
    score = _score_from_ratio(-avg_accrual, good=(0.02, 0.05), bad=(-0.03, 0.0))
    return round(score, 4)


def _compute_scores(payload: Dict[str, Any], red_flags: List[RedFlag]) -> Dict[str, float]:
    periods = payload.get("periods") or []
    if not periods:
        return {
            "earnings_quality": 0.0,
            "accrual_quality": 0.0,
            "cash_quality": 0.0,
            "balance_sheet_quality": 0.0,
            "governance_quality": 0.0,
            "overall": 0.0,
        }

    latest = _latest_period(periods)
    ni = latest.get("net_income")
    ocf = latest.get("operating_cash_flow")
    capex = latest.get("capex")
    equity = latest.get("equity")
    goodwill = latest.get("goodwill")
    cash = latest.get("cash")
    st_debt = latest.get("short_term_debt")
    total_debt = latest.get("total_debt")

    ocf_to_ni = _safe_div(ocf, ni)
    fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
    fcf_to_ni = _safe_div(fcf, ni)

    goodwill_to_equity = _safe_div(goodwill, equity)
    st_debt_to_cash = _safe_div(st_debt, cash)
    net_debt = (total_debt - cash) if (total_debt is not None and cash is not None) else None
    net_debt_to_equity = _safe_div(net_debt, equity)

    cash_score = (
        0.55 * _score_from_ratio(ocf_to_ni, good=(0.9, 1.2), bad=(0.3, 0.7))
        + 0.45 * _score_from_ratio(fcf_to_ni, good=(0.7, 1.0), bad=(0.1, 0.5))
    )

    bs_score = _clamp(
        0.5 * (1.0 - _score_from_ratio(goodwill_to_equity, good=(0.0, 0.05), bad=(0.35, 0.6)))
        + 0.5 * (1.0 - _score_from_ratio(net_debt_to_equity, good=(-0.2, 0.0), bad=(0.6, 1.2))),
        0.0, 1.0,
    )

    gov = payload.get("governance") or {}
    gov_score = 1.0
    if gov.get("audit_opinion") not in (None, "", "unqualified"):
        gov_score -= 0.5
    if gov.get("restatement_in_last_5y") is True:
        gov_score -= 0.25
    if gov.get("cfo_turnover_in_last_3y") is True:
        gov_score -= 0.10
    if gov.get("regulatory_inquiry_in_last_3y") is True:
        gov_score -= 0.10
    if gov.get("related_party_transactions_flag") is True:
        gov_score -= 0.10
    if gov.get("equity_pledge_flag") is True:
        gov_score -= 0.10
    gov_score = _clamp(gov_score, 0.0, 1.0)

    # 独立应计质量维度（Sloan 简化版）
    accrual_score = _compute_accrual_quality(periods)

    # earnings_quality = 应计质量 + 现金转化 + 治理基础的加权合成
    earnings_score = _clamp(0.40 * accrual_score + 0.40 * cash_score + 0.20 * gov_score, 0.0, 1.0)

    # red flag penalty（上限 0.25）
    penalty = min(
        sum(0.08 if r.severity == "high" else (0.04 if r.severity == "medium" else 0.02) for r in red_flags),
        0.25,
    )

    overall = _clamp(
        0.25 * earnings_score + 0.20 * accrual_score + 0.25 * cash_score + 0.20 * bs_score + 0.10 * gov_score - penalty,
        0.0, 1.0,
    )

    return {
        "earnings_quality": round(earnings_score, 4),
        "accrual_quality": round(accrual_score, 4),
        "cash_quality": round(cash_score, 4),
        "balance_sheet_quality": round(bs_score, 4),
        "governance_quality": round(gov_score, 4),
        "overall": round(overall, 4),
    }


def _grade_from_overall(overall: float) -> str:
    if overall >= 0.80:
        return "A"
    if overall >= 0.65:
        return "B"
    if overall >= 0.45:
        return "C"
    return "D"


def _build_verdict(payload: Dict[str, Any], scores: Dict[str, float], red_flags: List[RedFlag]) -> Dict[str, Any]:
    overall = float(scores.get("overall", 0.0))
    grade = _grade_from_overall(overall)

    key_uncertainties = []
    if len(payload.get("periods") or []) < 5:
        key_uncertainties.append("历史期间不足 5 年，部分红旗与趋势判断可能失真")

    if any(r.category == "revenue_quality" and r.severity in ("high", "medium") for r in red_flags):
        key_uncertainties.append("收入确认与回款匹配关系需进一步核验（应收与收入增速差异）")

    if any(r.rule_id in ("fq_cash_003t",) for r in red_flags):
        key_uncertainties.append("OCF/NI 趋势性下滑，需核查是否为结构性盈利质量问题")

    summary = "以应计质量、现金转化、资产负债表风险与治理基础信号为核心的 FQE MVP 结论。"
    if red_flags:
        summary += f" 当前命中红旗 {len(red_flags)} 项（含趋势），整体评分={overall:.2f}，等级={grade}。"

    confidence = 0.75
    if not payload.get("governance"):
        confidence -= 0.15
    high_cnt = sum(1 for r in red_flags if r.severity == "high")
    confidence -= min(0.20, 0.05 * high_cnt)
    confidence = _clamp(confidence, 0.3, 0.9)

    return {
        "key_strengths": [],
        "key_uncertainties": key_uncertainties,
        "verdict": {"grade": grade, "summary": summary, "confidence": round(confidence, 4)},
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="FQE MVP: generate adjustments/red_flags/verdict JSON from financial facts")
    ap.add_argument("--input", required=True, help="Path to financial facts JSON")
    ap.add_argument(
        "--rules",
        required=False,
        help="Path to rules JSON. Default: skills/financial-quality-engine/rules/fqe_mvp_rules.json (relative to this script).",
    )
    ap.add_argument(
        "--case",
        required=False,
        help="Case directory path (e.g. research_cases/case_YYYYMMDD_company). Outputs follow the deep research case structure.",
    )
    ap.add_argument("--outdir", required=False, help="Output directory (legacy mode, ignored if --case is provided).")
    args = ap.parse_args()

    input_path = Path(args.input)
    case_dir: Optional[Path] = Path(args.case) if args.case else None
    default_rules_path = Path(__file__).resolve().parent.parent / "rules" / "fqe_mvp_rules.json"
    rules_path = Path(args.rules) if args.rules else default_rules_path
    rules = _load_rules(rules_path)

    if case_dir is not None:
        normalized_dir = case_dir / "normalized"
        fq_dir = case_dir / "financial_quality"
        raw_dir = case_dir / "raw"
        for p in [
            raw_dir / "filings",
            raw_dir / "market",
            raw_dir / "industry",
            normalized_dir,
            fq_dir,
            case_dir / "integrated",
        ]:
            p.mkdir(parents=True, exist_ok=True)
        # competitive_positioning/ 不默认创建；FQE-only 流程不应触发 CPE Warning
        out_adjustments = fq_dir / "adjustments.json"
        out_red_flags = fq_dir / "red_flags.json"
        out_verdict = fq_dir / "verdict.json"
        out_evidence = normalized_dir / "evidence.jsonl"
        out_normalized_financial_facts = normalized_dir / "financial_facts.json"
    else:
        if not args.outdir:
            raise ValueError("Either --case or --outdir must be provided")
        outdir = Path(args.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        out_adjustments = outdir / "adjustments.json"
        out_red_flags = outdir / "red_flags.json"
        out_verdict = outdir / "verdict.json"
        out_evidence = outdir / "evidence.jsonl"
        out_normalized_financial_facts = outdir / "financial_facts.json"

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    company = payload.get("company", "")
    as_of_date = payload.get("as_of_date", "")

    periods = payload.get("periods") or []
    if not periods:
        raise ValueError("Input missing periods[]")

    latest = _latest_period(periods)
    reported_ni = float(latest.get("net_income") or 0.0)

    adjustments = _build_adjustments(payload)
    adjusted_ni = _apply_adjustments_to_net_income(reported_ni, adjustments)

    red_flags = _compute_red_flags(payload, rules)
    _rewrite_red_flag_refs_to_evidence_ids(payload, red_flags)
    scores = _compute_scores(payload, red_flags)
    verdict_pack = _build_verdict(payload, scores, red_flags)
    evidence = _build_min_evidence(payload, red_flags)

    adjustments_out = {
        "company": company,
        "as_of_date": as_of_date,
        "reported_net_income": reported_ni,
        "adjusted_net_income": adjusted_ni,
        "adjustments": adjustments,
    }

    verdict_out = {
        "company": company,
        "as_of_date": as_of_date,
        "normalized_earnings": {
            "reported_net_income": reported_ni,
            "adjusted_net_income": adjusted_ni,
            "adjustments": adjustments,
        },
        "scores": scores,
        "score_metadata": {
            "accrual_quality": {
                "formula": "(NI - OCF) / avg_total_assets，均值后取反映射到 [0,1]",
                "denominator_priority": "total_assets > equity（fallback）",
                "good_anchor": "avg_accrual_ratio <= -0.02",
                "bad_anchor": "avg_accrual_ratio >= 0.08",
            },
            "cash_quality": {"formula": "0.55 * score(OCF/NI) + 0.45 * score(FCF/NI)"},
            "balance_sheet_quality": {"formula": "0.5 * (1 - score(goodwill/equity)) + 0.5 * (1 - score(net_debt/equity))"},
            "earnings_quality": {"formula": "0.40 * accrual_quality + 0.40 * cash_quality + 0.20 * governance_quality"},
            "overall": {
                "formula": "0.25*earnings + 0.20*accrual + 0.25*cash + 0.20*bs + 0.10*gov - penalty",
                "penalty_cap": 0.25,
                "penalty_per_high_flag": 0.08,
                "penalty_per_medium_flag": 0.04,
            },
        },
        "red_flags": [r.to_dict() for r in red_flags],
        "key_strengths": verdict_pack["key_strengths"],
        "key_uncertainties": verdict_pack["key_uncertainties"],
        "verdict": {
            **verdict_pack["verdict"],
            "grade_thresholds": {"A": 0.80, "B": 0.65, "C": 0.45, "D": 0.0},
        },
    }

    out_normalized_financial_facts.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_adjustments.write_text(json.dumps(adjustments_out, ensure_ascii=False, indent=2), encoding="utf-8")
    out_red_flags.write_text(
        json.dumps({"company": company, "as_of_date": as_of_date, "red_flags": [r.to_dict() for r in red_flags]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    out_verdict.write_text(json.dumps(verdict_out, ensure_ascii=False, indent=2), encoding="utf-8")
    out_evidence.write_text(
        "\n".join([e.to_jsonl() for e in evidence]) + ("\n" if evidence else ""),
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
