import unittest
import numpy as np
import pandas as pd

from src.temporal_calibration import temporal_temperature_calibration, _temperature_transform


class TestTemporalTemperatureCalibration(unittest.TestCase):
    def test_temperature_transform_preserves_simplex_and_order(self):
        probs = np.array([[0.6, 0.25, 0.15], [0.2, 0.5, 0.3]])
        calibrated = _temperature_transform(probs, 1.3)
        self.assertTrue(np.allclose(calibrated.sum(axis=1), 1.0))
        self.assertTrue(np.all((calibrated >= 0) & (calibrated <= 1)))
        self.assertEqual(np.argmax(probs, axis=1).tolist(), np.argmax(calibrated, axis=1).tolist())

    def test_uses_only_earlier_seasons_for_each_holdout(self):
        rows = []
        seasons = ["2023-24", "2024-25", "2025-26"]
        for season, actual in zip(seasons, ["1", "X", "2"]):
            rows.append({"season": season, "actual_1X2": actual,
                         "model_p1": 0.6, "model_px": 0.25, "model_p2": 0.15})
        result = temporal_temperature_calibration(pd.DataFrame(rows), ["model"])
        self.assertEqual(set(result["Temporada_prueba"]), {"2024-25", "2025-26"})
        first = result[result["Temporada_prueba"] == "2024-25"]
        second = result[result["Temporada_prueba"] == "2025-26"]
        self.assertEqual(set(first["Temporadas_entrenamiento"]), {"2023-24"})
        self.assertEqual(set(second["Temporadas_entrenamiento"]), {"2023-24, 2024-25"})
        self.assertTrue((result["N_prueba"] == 1).all())
        self.assertTrue((result["Control_fuga"].str.contains("estrictamente anteriores")).all())

    def test_empty_input_returns_schema(self):
        result = temporal_temperature_calibration(pd.DataFrame(), ["model"])
        self.assertIn("Temperatura_elegida", result.columns)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
