import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "src" / "backtest_openfootball.py"
SPEC = importlib.util.spec_from_file_location("backtest_openfootball", SCRIPT)
bt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bt)


class TestOpenFootballBacktest(unittest.TestCase):
    def test_poisson_distribution_is_normalized(self):
        probs = bt.poisson(1.7)
        self.assertEqual(len(probs), 13)  # goals 0 through 12 inclusive
        self.assertAlmostEqual(sum(probs), 1.0, places=12)
        self.assertTrue(all(p >= 0 for p in probs))

    def test_1x2_probabilities_are_normalized(self):
        probs = bt.p1x2(1.4, 0.9)
        self.assertEqual(len(probs), 3)
        self.assertAlmostEqual(sum(probs), 1.0, places=12)
        self.assertTrue(all(0 <= p <= 1 for p in probs))

    def test_clean_removes_exact_duplicate_and_invalid_score(self):
        base = {
            "league": "Premier League", "season": "2024-25",
            "date": "2024-08-17", "home": "Home FC", "away": "Away FC",
            "hg": 2, "ag": 1
        }
        rows = [base.copy(), base.copy(), {**base, "date": "bad-date"}]
        clean, invalid, duplicates, conflicts = bt.clean(rows)
        self.assertEqual(len(clean), 1)
        self.assertEqual(len(invalid), 1)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(conflicts), 0)

    def test_clean_excludes_conflicting_scores_for_same_fixture(self):
        base = {
            "league": "LaLiga", "season": "2024-25",
            "date": "2024-08-17", "home": "Home FC", "away": "Away FC",
            "hg": 2, "ag": 1
        }
        rows = [base.copy(), {**base, "hg": 0, "ag": 0}]
        clean, invalid, duplicates, conflicts = bt.clean(rows)
        self.assertEqual(len(clean), 0)
        self.assertEqual(len(conflicts), 2)


if __name__ == "__main__":
    unittest.main()
