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

    def test_probabilities_are_finite_and_normalized_across_rates(self):
        for lh in (0.05, 0.2, 1.0, 2.5, 5.0, 10.0):
            for la in (0.05, 0.4, 1.8, 4.0, 9.0):
                probs = bt.p1x2(lh, la)
                self.assertEqual(len(probs), 3)
                self.assertTrue(all(__import__("math").isfinite(p) for p in probs))
                self.assertTrue(all(0 <= p <= 1 for p in probs))
                self.assertAlmostEqual(sum(probs), 1.0, places=12)

    def test_backtest_is_deterministic_and_future_scores_do_not_change_past_prediction(self):
        rows = []
        # Five prior fixtures for each side, then the target fixture.
        for i in range(5):
            rows.append({
                "league": "Premier League", "season": "2023-24",
                "date": f"2024-01-{i+1:02d}", "home": "A", "away": f"Opponent{i}",
                "hg": 1 + (i % 2), "ag": i % 2
            })
            rows.append({
                "league": "Premier League", "season": "2023-24",
                "date": f"2024-01-{i+1:02d}", "home": f"Visitor{i}", "away": "B",
                "hg": i % 2, "ag": 1 + (i % 2)
            })
        target = {
            "league": "Premier League", "season": "2023-24",
            "date": "2024-01-10", "home": "A", "away": "B", "hg": 1, "ag": 0
        }
        future = {
            "league": "Premier League", "season": "2023-24",
            "date": "2024-01-11", "home": "A", "away": "B", "hg": 9, "ag": 0
        }
        clean1, *_ = bt.clean(rows + [target, future])
        detail1, _ = bt.backtest(clean1)
        clean2, *_ = bt.clean(rows + [target, {**future, "hg": 0, "ag": 9}])
        detail2, _ = bt.backtest(clean2)
        target1 = detail1[detail1["date"] == __import__("pandas").Timestamp("2024-01-10")]
        target2 = detail2[detail2["date"] == __import__("pandas").Timestamp("2024-01-10")]
        self.assertEqual(len(target1), 1)
        self.assertEqual(len(target2), 1)
        for col in ("multipliers_1.10_0.90_p1", "multipliers_1.10_0.90_px",
                    "multipliers_1.10_0.90_p2"):
            self.assertAlmostEqual(float(target1.iloc[0][col]), float(target2.iloc[0][col]), places=12)
        self.assertEqual(len(detail1), len(detail2))


if __name__ == "__main__":
    unittest.main()
