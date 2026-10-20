#!/usr/bin/env python3
"""Temporal exploratory backtest for Colombia Primera A using OpenFootball text data.

This script intentionally evaluates only completed matches with a parseable final score.
It does not use odds and does not claim profitability. 2025 source currently contains
only the Apertura section, so coverage is reported rather than silently treated as a
complete calendar year.
"""
from __future__ import annotations
import datetime as dt
import json
import math
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "evaluacion" / "backtest_liga_betplay_2023_2025.json"
REPORT = ROOT / "data" / "evaluacion" / "backtest_liga_betplay_2023_2025.md"
SOURCES = {
    2023: "https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2023_co1.txt",
    2024: "https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2024_co1.txt",
    2025: "https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2025_co1.txt",
}
DATE_RE = re.compile(r"^\s{2,}(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
MATCH_RE = re.compile(r"^\s{2,}(\d{1,2}:\d{2})\s+(.+?)\s+v\s+(.+?)\s+(\d+)-(\d+)(?:\s|$)")

def fetch_season(year: int) -> str:
    req = urllib.request.Request(SOURCES[year], headers={"User-Agent": "football-model-research/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")

def parse_matches(year: int, content: str):
    current_date = None
    rows = []
    for line in content.splitlines():
        dm = DATE_RE.match(line)
        if dm:
            month = dt.datetime.strptime(dm.group(1), "%b").month
            day = int(dm.group(2))
            y = int(dm.group(3)) if dm.group(3) else year
            try:
                current_date = dt.date(y, month, day)
            except ValueError:
                continue
            continue
        mm = MATCH_RE.match(line)
        if not mm or current_date is None:
            continue
        home, away = mm.group(2).strip(), mm.group(3).strip()
        hg, ag = int(mm.group(4)), int(mm.group(5))
        # Exclude penalty shootouts and only use the final score before any parentheses.
        if not home or not away:
            continue
        rows.append({"date": current_date.isoformat(), "home": home, "away": away,
                     "hg": hg, "ag": ag, "season_source": year})
    return rows

def poisson(lam, max_goals=12):
    p = [math.exp(-lam)]
    for k in range(1, max_goals + 1):
        p.append(p[-1] * lam / k)
    z = sum(p)
    return [v / z for v in p]

def probs(lh, la):
    ph, pa = poisson(lh), poisson(la)
    p1x2 = [0.0, 0.0, 0.0]
    markets = {"over15": 0.0, "under35": 0.0, "btts": 0.0}
    for h, hp in enumerate(ph):
        for a, ap in enumerate(pa):
            p = hp * ap
            p1x2[0 if h > a else 1 if h == a else 2] += p
            if h + a >= 2: markets["over15"] += p
            if h + a <= 3: markets["under35"] += p
            if h > 0 and a > 0: markets["btts"] += p
    return p1x2, markets

def logloss(p, y):
    return -math.log(max(1e-12, min(1-1e-12, p[y])))

def main():
    all_rows, coverage = [], {}
    for year in SOURCES:
        text = fetch_season(year)
        parsed = parse_matches(year, text)
        coverage[str(year)] = {"parsed_scored_matches": len(parsed), "source_url": SOURCES[year]}
        all_rows.extend(parsed)
    all_rows.sort(key=lambda x: (x["date"], x["home"], x["away"]))
    history = defaultdict(list)
    scored = []
    for row in all_rows:
        # Build prediction only from prior completed matches, before updating either team.
        home_hist, away_hist = history[row["home"]], history[row["away"]]
        if len(home_hist) < 4 or len(away_hist) < 4:
            # still add result to future history below
            pass
        else:
            hh, ah = home_hist[-10:], away_hist[-10:]
            # Team scoring/conceding rates from recent matches; home/away split is unavailable
            # in the source parser and is therefore not falsely claimed.
            h_for = sum(x["gf"] for x in hh) / len(hh)
            h_against = sum(x["ga"] for x in hh) / len(hh)
            a_for = sum(x["gf"] for x in ah) / len(ah)
            a_against = sum(x["ga"] for x in ah) / len(ah)
            # Shrink small samples toward league-wide pre-match averages.
            prev = [x for x in scored if x["date"] < row["date"]]
            if len(prev) >= 20:
                mean_home = sum(x["hg"] for x in prev) / len(prev)
                mean_away = sum(x["ag"] for x in prev) / len(prev)
            else:
                mean_home, mean_away = 1.35, 1.05
            strength = 4.0
            lh = max(0.15, (h_for * a_against + strength * mean_home) / (strength + 1))
            la = max(0.15, (a_for * h_against + strength * mean_away) / (strength + 1))
            p1x2, pm = probs(lh, la)
            y1x2 = 0 if row["hg"] > row["ag"] else 1 if row["hg"] == row["ag"] else 2
            scored.append({**row, "lambda_home": lh, "lambda_away": la,
                           "p1x2": p1x2, "markets": pm, "y1x2": y1x2})
        history[row["home"]].append({"gf": row["hg"], "ga": row["ag"], "date": row["date"]})
        history[row["away"]].append({"gf": row["ag"], "ga": row["hg"], "date": row["date"]})
    n = len(scored)
    if not n:
        raise SystemExit("No se pudieron generar predicciones; revisar formato/fuente.")
    brier_1x2 = sum(sum((p[i] - (i == r["y1x2"]))**2 for i in range(3)) for r in scored) / n
    ll_1x2 = sum(logloss(r["p1x2"], r["y1x2"]) for r in scored) / n
    metrics = {"1x2": {"n": n, "brier_multiclass": brier_1x2, "log_loss": ll_1x2,
                       "accuracy": sum(max(range(3), key=lambda i: r["p1x2"][i]) == r["y1x2"] for r in scored)/n}}
    for key, outcome in [("over15", lambda r: int(r["hg"] + r["ag"] >= 2)),
                         ("under35", lambda r: int(r["hg"] + r["ag"] <= 3)),
                         ("btts", lambda r: int(r["hg"] > 0 and r["ag"] > 0))]:
        brier = sum((r["markets"][key] - outcome(r))**2 for r in scored)/n
        ll = sum(logloss([1-r["markets"][key], r["markets"][key]], outcome(r)) for r in scored)/n
        metrics[key] = {"n": n, "brier": brier, "log_loss": ll,
                        "mean_probability": sum(r["markets"][key] for r in scored)/n,
                        "observed_rate": sum(outcome(r) for r in scored)/n}
    payload = {"status": "exploratory_not_calibrated", "method": "rolling chronological, last 10 results per team, minimum 4 prior matches, shrinkage strength 4; final-score-only source",
               "source_coverage": coverage, "evaluated_matches": n, "metrics": metrics,
               "limitations": ["source coverage is not guaranteed complete", "team names may change across seasons",
                               "source does not provide kickoff times or historical pre-match odds",
                               "home/away split within team form is not modeled in this first diagnostic",
                               "2025 file is partial season in current source", "not an ROI evaluation"]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Backtest exploratorio — Liga BetPlay 2023–2025", "",
             "**Estado:** diagnóstico exploratorio; no representa calibración aprobada ni rentabilidad.", "",
             "## Cobertura de la fuente", ""]
    for y, d in coverage.items(): lines.append(f"- {y}: {d['parsed_scored_matches']} marcadores parseados — {d['source_url']}")
    lines += ["", f"- Predicciones evaluadas fuera de muestra: **{n}**.", "",
              "## Métricas", "", "| Mercado | N | Brier | Log loss | Prob. media | Frecuencia real |", "|---|---:|---:|---:|---:|---:|"]
    for key, label in [("1x2","1X2"),("over15","Over 1.5"),("under35","Under 3.5"),("btts","Ambos marcan")]:
        m=metrics[key]
        lines.append(f"| {label} | {m['n']} | {m.get('brier_multiclass',m.get('brier',0)):.6f} | {m['log_loss']:.6f} | {m.get('mean_probability',float('nan')):.4f} | {m.get('observed_rate',float('nan')):.4f} |")
    lines += ["", "## Limitaciones y siguiente paso", "",
              "Esta primera ejecución, si la fuente se descarga y parsea sin errores, solo ofrece un diagnóstico. Verificar la cobertura, alias de equipos, formato de fechas y scores de playoffs. El modelo no incorpora datos en vivo, cuotas ni estadísticas avanzadas. Antes de desplegar una recalibración, comparar en el mismo conjunto temporal con una línea base de frecuencias de competición y producir tablas de calibración e intervalos de confianza. No usar este informe para afirmar valor esperado positivo.", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
