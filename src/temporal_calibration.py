"""Leakage-safe temporal temperature scaling for 1X2 backtests."""
import numpy as np
import pandas as pd

LABELS = ("1", "X", "2")
PROB_SUFFIXES = ("p1", "px", "p2")


def _normalized_probs(values):
    p = np.clip(np.asarray(values, dtype=float), 1e-12, 1.0)
    return p / p.sum(axis=1, keepdims=True)


def _temperature_transform(probs, temperature):
    """Transform probabilities while preserving a normalized 1X2 vector."""
    logits = np.log(_normalized_probs(probs)) / float(temperature)
    logits -= logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def _indices(actual):
    return np.array([LABELS.index(str(x)) for x in actual], dtype=int)


def _logloss(probs, actual):
    idx = _indices(actual)
    return float(-np.log(np.clip(probs[np.arange(len(idx)), idx], 1e-15, 1)).mean())


def _metrics(probs, actual):
    idx = _indices(actual)
    onehot = np.eye(3)[idx]
    return {
        "Exactitud": float((np.argmax(probs, axis=1) == idx).mean()),
        "Brier": float(((probs - onehot) ** 2).sum(axis=1).mean()),
        "LogLoss": _logloss(probs, actual),
    }


def temporal_temperature_calibration(detail, models, temperatures=None):
    """Fit temperature on past seasons and report metrics on the next season.

    Each holdout uses only strictly earlier season labels for fitting. The first
    available season is training-only; no holdout result is reported for it.
    """
    columns = [
        "Modelo", "Temporada_prueba", "Temporadas_entrenamiento",
        "N_entrenamiento", "N_prueba", "Temperatura_elegida",
        "LogLoss_entrenamiento_original", "LogLoss_entrenamiento_calibrado",
        "Metrica", "Original", "Calibrado", "Cambio_calibrado_menos_original",
        "Metodo", "Control_fuga",
    ]
    if detail.empty:
        return pd.DataFrame(columns=columns)
    temps = np.asarray(temperatures if temperatures is not None
                       else np.linspace(0.50, 2.50, 81), dtype=float)
    seasons = sorted(detail["season"].dropna().astype(str).unique())
    rows = []
    for target_index in range(1, len(seasons)):
        target_season = seasons[target_index]
        train_seasons = seasons[:target_index]
        train = detail[detail["season"].astype(str).isin(train_seasons)]
        test = detail[detail["season"].astype(str) == target_season]
        if train.empty or test.empty:
            continue
        actual_train = train["actual_1X2"].astype(str).to_numpy()
        actual_test = test["actual_1X2"].astype(str).to_numpy()
        for model in models:
            cols = [f"{model}_{suffix}" for suffix in PROB_SUFFIXES]
            p_train = _normalized_probs(train[cols].to_numpy(dtype=float))
            p_test = _normalized_probs(test[cols].to_numpy(dtype=float))
            train_scores = [(_logloss(_temperature_transform(p_train, t), actual_train), float(t))
                            for t in temps]
            train_loss, chosen_t = min(train_scores, key=lambda item: (item[0], item[1]))
            calibrated_test = _temperature_transform(p_test, chosen_t)
            original_metrics = _metrics(p_test, actual_test)
            calibrated_metrics = _metrics(calibrated_test, actual_test)
            for metric in ("Exactitud", "Brier", "LogLoss"):
                original = original_metrics[metric]
                calibrated = calibrated_metrics[metric]
                rows.append({
                    "Modelo": model,
                    "Temporada_prueba": target_season,
                    "Temporadas_entrenamiento": ", ".join(train_seasons),
                    "N_entrenamiento": len(train),
                    "N_prueba": len(test),
                    "Temperatura_elegida": chosen_t,
                    "LogLoss_entrenamiento_original": _logloss(p_train, actual_train),
                    "LogLoss_entrenamiento_calibrado": train_loss,
                    "Metrica": metric,
                    "Original": original,
                    "Calibrado": calibrated,
                    "Cambio_calibrado_menos_original": calibrated - original,
                    "Metodo": "Temperature scaling multinomial; rejilla 0.50–2.50",
                    "Control_fuga": "Ajuste solo con temporadas estrictamente anteriores",
                })
    return pd.DataFrame(rows, columns=columns)
