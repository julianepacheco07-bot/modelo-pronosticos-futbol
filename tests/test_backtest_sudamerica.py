import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / "src" / "backtest_sudamerica.py"
SPEC = importlib.util.spec_from_file_location("backtest_sudamerica", SCRIPT)
bt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bt)


class TestSouthAmericaBacktest(unittest.TestCase):
    def test_parse_txt_extracts_final_score_and_year(self):
        source = """  Sat Aug 17 2024
    16:00 Team Alpha v Team Beta 2-1
"""
        rows = bt.parse_txt(source, "League", "2023")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2024-08-17")
        self.assertEqual((rows[0]["hg"], rows[0]["ag"]), (2, 1))

    def test_poisson_and_market_probabilities_are_valid(self):
        p = bt.poisson(1.4)
        self.assertAlmostEqual(sum(p), 1.0, places=12)
        self.assertTrue(all(0 <= x <= 1 for x in p))
        hist = pd.DataFrame([
            {"home":"A","away":f"X{i}","hg":2,"ag":0} for i in range(15)
        ] + [
            {"home":f"Y{i}","away":"B","hg":0,"ag":1} for i in range(15)
        ])
        match = SimpleNamespace(home="A", away="B")
        pred = bt.predict(hist, match)
        self.assertIsNotNone(pred)
        for key in ("p_over_1_5", "p_under_3_5", "p_btts_yes"):
            self.assertTrue(0 <= pred[key] <= 1)

    def test_insufficient_history_is_skipped(self):
        hist = pd.DataFrame([{"home":"A","away":"B","hg":1,"ag":0}])
        self.assertIsNone(bt.predict(hist, SimpleNamespace(home="A", away="B")))

    def test_binary_metrics_are_finite_at_probability_edges(self):
        for p in (0.0, 1.0, 0.5):
            brier, logloss = bt.score(p, 1)
            self.assertTrue(brier >= 0)
            self.assertTrue(logloss >= 0)
            self.assertTrue(pd.notna(logloss))


if __name__ == "__main__":
    unittest.main()
