"""Probability helpers for Betano football market labels.

Probabilities are model inputs, not bookmaker prices. The two-goal-lead
settlement is modeled as: selected team wins at full time OR reaches a
two-goal lead at any point. Use only pre-match goal-rate estimates.
"""
from __future__ import annotations

import math
import re
import unicodedata
from typing import Dict, Optional


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


def poisson_probs(lam: float, max_goals: int = 12) -> list[float]:
    if lam < 0 or max_goals < 1:
        raise ValueError("lambda debe ser >= 0 y max_goals >= 1")
    p = [math.exp(-lam)]
    for k in range(1, max_goals + 1):
        p.append(p[-1] * lam / k)
    total = sum(p)
    return [x / total for x in p]


def scoreline_markets(lambda_home: float, lambda_away: float) -> Dict[str, float]:
    """Independent Poisson scoreline estimates; no calibration implied."""
    if lambda_home < 0 or lambda_away < 0:
        raise ValueError("Las tasas de gol no pueden ser negativas")
    home, away = poisson_probs(lambda_home), poisson_probs(lambda_away)
    home_win = draw = away_win = over15 = under35 = btts = 0.0
    for i, pi in enumerate(home):
        for j, pj in enumerate(away):
            p = pi * pj
            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p
            if i + j >= 2:
                over15 += p
            if i + j <= 3:
                under35 += p
            if i > 0 and j > 0:
                btts += p
    return {
        "home_win": home_win, "draw": draw, "away_win": away_win,
        "1x": home_win + draw, "x2": away_win + draw,
        "12": home_win + away_win, "over_1_5": over15,
        "under_3_5": under35, "btts_yes": btts,
    }


def win_or_two_goal_lead(lambda_selected: float, lambda_opponent: float,
                         minutes: int = 90) -> float:
    """P(selected wins FT OR leads by >=2 at any point).

    A minute-step Poisson-arrival approximation is used. At each minute,
    each side can score zero or one goal with probability lambda/minutes;
    simultaneous goals are allowed as an approximation. The state tracks
    goal difference and whether the selected side has ever led by 2.
    This is an exploratory estimate and needs calibration/backtesting.
    """
    if lambda_selected < 0 or lambda_opponent < 0 or minutes < 1:
        raise ValueError("Tasas no negativas y minutes >= 1 requeridos")
    ps = min(lambda_selected / minutes, 1.0)
    po = min(lambda_opponent / minutes, 1.0)
    # State: (goal difference, has reached +2); probability mass.
    states: Dict[tuple[int, bool], float] = {(0, False): 1.0}
    for _ in range(minutes):
        nxt: Dict[tuple[int, bool], float] = {}
        outcomes = ((0, 0, (1-ps)*(1-po)),
                    (1, 0, ps*(1-po)),
                    (0, 1, (1-ps)*po),
                    (1, 1, ps*po))
        for (diff, reached), mass in states.items():
            for sh, sa, prob in outcomes:
                nd = diff + sh - sa
                nr = reached or nd >= 2
                key = (nd, nr)
                nxt[key] = nxt.get(key, 0.0) + mass * prob
        states = nxt
    return min(1.0, sum(m for (d, reached), m in states.items()
                        if reached or d > 0))


def implied_probability(odds: float) -> float:
    """Raw break-even probability; does not remove bookmaker margin."""
    if odds <= 1:
        raise ValueError("La cuota decimal debe ser > 1")
    return 1.0 / odds


def expected_value_per_unit(probability: float, odds: float) -> float:
    """Binary full-win/full-loss EV per unit stake, before promotions/taxes."""
    if not 0 <= probability <= 1 or odds <= 1:
        raise ValueError("Probabilidad entre 0 y 1 y cuota > 1 requeridas")
    return probability * odds - 1.0


def classify(probability: Optional[float], odds: Optional[float],
             min_probability: float = 0.75) -> str:
    """Never confuse missing odds/probability with a negative-EV decision."""
    if probability is None:
        return "ANALISIS_INSUFICIENTE"
    if odds is None:
        return "CUOTA_PENDIENTE"
    if not 0 <= probability <= 1 or odds <= 1:
        raise ValueError("Probabilidad o cuota fuera de rango")
    if probability >= min_probability and expected_value_per_unit(probability, odds) > 0:
        return "APUESTA_CANDIDATA"
    return "NO BET"


def infer_market(label: str) -> dict:
    """Interpret common market names; ambiguous wording stays unresolved."""
    s = _norm(label)
    if ("liderar por 2 goles" in s or "ventaja de 2 goles" in s
            or "2 goles de ventaja" in s):
        return {"market": "win_or_two_goal_lead",
                "settlement": "win at full time OR lead by >=2 at any time",
                "rule_source": "reported by user; official Colombia terms still to verify"}
    if "doble oportunidad" in s or re.search(r"(^| )1x($| )", s):
        return {"market": "1x", "settlement": "home win or draw"}
    if re.search(r"(^| )x2($| )", s) or "gana o empata" in s:
        return {"market": "x2", "settlement": "selected team wins or match draws"}
    if re.search(r"(^| )12($| )", s):
        return {"market": "12", "settlement": "either team wins; draw loses"}
    if "ambos marcan" in s or "btts si" in s:
        return {"market": "btts_yes", "settlement": "both teams score at least one goal"}
    if "mas de 1 5" in s or "over 1 5" in s:
        return {"market": "over_1_5", "settlement": "at least 2 total goals"}
    if "menos de 3 5" in s or "under 3 5" in s:
        return {"market": "under_3_5", "settlement": "at most 3 total goals"}
    if "victoria" in s or "ganar el partido" in s or "ganador" in s:
        return {"market": "team_win", "settlement": "selected team wins at full time"}
    return {"market": None, "settlement": None,
            "status": "PENDIENTE_DE_VERIFICACION",
            "reason": "Market label is not unambiguous enough to infer settlement safely"}
