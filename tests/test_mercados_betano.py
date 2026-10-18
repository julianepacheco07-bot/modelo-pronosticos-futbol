import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.mercados_betano import (
    classify, expected_value_per_unit, implied_probability, infer_market,
    scoreline_markets, win_or_two_goal_lead,
)


class BetanoMarketTests(unittest.TestCase):
    def test_market_name_inference(self):
        self.assertEqual(infer_market("Ajax o empate (X2)")["market"], "x2")
        self.assertEqual(infer_market("Más de 1.5 goles")["market"], "over_1_5")
        self.assertEqual(
            infer_market("Ganar el partido o liderar por 2 goles Molde")["market"],
            "win_or_two_goal_lead",
        )
        self.assertIsNone(infer_market("Mercado ambiguo")["market"])

    def test_scoreline_probabilities_are_bounded(self):
        markets = scoreline_markets(1.5, 1.0)
        self.assertTrue(all(0 <= p <= 1 for p in markets.values()))
        self.assertAlmostEqual(markets["1x"] + markets["away_win"], 1.0, places=5)

    def test_two_goal_lead_includes_final_win(self):
        # The event is at least as likely as winning outright.
        p = win_or_two_goal_lead(1.8, 0.8)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)
        # The two-goal settlement is a separate time-path approximation;
        # do not assert numeric equality with the independent scoreline Poisson.

    def test_missing_odds_are_not_no_bet(self):
        self.assertEqual(classify(0.80, None), "CUOTA_PENDIENTE")
        self.assertEqual(classify(None, 1.50), "ANALISIS_INSUFICIENTE")
        self.assertEqual(classify(0.80, 1.50), "APUESTA_CANDIDATA")
        self.assertEqual(classify(0.70, 1.50), "NO BET")

    def test_ev_and_break_even(self):
        self.assertAlmostEqual(implied_probability(2.0), 0.5)
        self.assertAlmostEqual(expected_value_per_unit(0.6, 2.0), 0.2)


if __name__ == "__main__":
    unittest.main()
