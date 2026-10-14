"""Pruebas básicas: python -m unittest tests/test_backtest_temporal.py"""
import unittest
import pandas as pd
import numpy as np
import ejecutar_backtest_multitemporada as bt

class BacktestTests(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        p = bt.probs_1x2(1.45, 1.10)
        self.assertEqual(len(p), 3)
        self.assertTrue(np.all((p >= 0) & (p <= 1)))
        self.assertAlmostEqual(float(p.sum()), 1.0, places=12)

    def test_identical_duplicate_removed_and_conflicting_fixture_excluded(self):
        base = {"league":"Test","season":"2425","date":pd.Timestamp("2025-01-01"),
                "date_raw":"2025-01-01","home":"A","away":"B","source_url":"test://fixture",
                "source_file":"test.csv","source_sha256":"abc","downloaded_utc":"test",
                "source_license":"test"}
        rows = [{**base,"hg":1,"ag":0},{**base,"hg":1,"ag":0},
                {**base,"hg":2,"ag":0},{**base,"date":pd.Timestamp("2025-01-08"),"home":"B","away":"A","hg":0,"ag":1}]
        clean,bad,nonint,dups,conflicts = bt.clean_data(pd.DataFrame(rows))
        self.assertEqual(len(dups),1)
        self.assertEqual(len(conflicts),2)
        self.assertEqual(len(clean),1)
        self.assertTrue(bad.empty)
        self.assertTrue(nonint.empty)

if __name__ == "__main__":
    unittest.main()
