#!/usr/bin/env python3
"""Registro prospectivo de cuotas y resultados de la simulación.

Solo registra cuotas capturadas desde el inicio del proyecto; no importa ni reconstruye
cuotas históricas previas. Una fila por selección/mercado y casa.
"""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "data" / "simulacion" / "registro_cuotas.csv"
FIELDS = [
    "id", "captured_at_utc", "match_date_local", "competition", "home_team",
    "away_team", "bookmaker", "market", "selection", "decimal_odds",
    "model_probability", "fair_odds", "expected_value", "status",
    "stake_units", "result", "profit_units", "notes"
]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--match-date", required=True, help="Fecha/hora local del partido, ISO 8601")
    p.add_argument("--competition", required=True)
    p.add_argument("--home", required=True)
    p.add_argument("--away", required=True)
    p.add_argument("--bookmaker", required=True, help="Casa de apuestas realmente observada")
    p.add_argument("--market", required=True)
    p.add_argument("--selection", required=True)
    p.add_argument("--odds", type=float, required=True, help="Cuota decimal observada ahora")
    p.add_argument("--probability", type=float, required=True, help="Probabilidad del modelo entre 0 y 1")
    p.add_argument("--status", default="PAPER_CANDIDATE", choices=["PAPER_CANDIDATE", "NO_BET", "INSUFFICIENT_DATA"])
    p.add_argument("--stake", type=float, default=1.0, help="Unidades virtuales; 0 si no se simula")
    p.add_argument("--notes", default="")
    a = p.parse_args()
    if a.odds <= 1:
        p.error("--odds debe ser mayor que 1")
    if not 0 < a.probability < 1:
        p.error("--probability debe estar entre 0 y 1")
    if a.stake < 0:
        p.error("--stake no puede ser negativa")
    fair = 1 / a.probability
    ev = a.probability * a.odds - 1
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    is_new = not LEDGER.exists()
    row = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "match_date_local": a.match_date, "competition": a.competition,
        "home_team": a.home, "away_team": a.away, "bookmaker": a.bookmaker,
        "market": a.market, "selection": a.selection, "decimal_odds": f"{a.odds:.4f}",
        "model_probability": f"{a.probability:.6f}", "fair_odds": f"{fair:.4f}",
        "expected_value": f"{ev:.6f}", "status": a.status, "stake_units": f"{a.stake:.2f}",
        "result": "PENDING", "profit_units": "", "notes": a.notes
    }
    with LEDGER.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            w.writeheader()
        w.writerow(row)
    print(f"Registro guardado: {LEDGER.relative_to(ROOT)}")
    print(f"Cuota={a.odds:.4f} | p_modelo={a.probability:.4%} | cuota_justa={fair:.4f} | EV={ev:.2%}")
    print("Resultado=PENDING; registrar solo cuando termine el partido. ROI no se calcula hasta liquidar selecciones.")

if __name__ == "__main__":
    main()
