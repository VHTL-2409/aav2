# core/forecaster.py
import numpy as np
import pandas as pd
from typing import Tuple

# Try to import statsmodels ARIMA optionally. If not present, fall back to a simple forecaster.
try:
    from statsmodels.tsa.arima.model import ARIMA  # type: ignore
    ARIMA_AVAILABLE = True
except Exception:
    ARIMA_AVAILABLE = False


class Forecaster:
    @staticmethod
    def forecast(
        historical: pd.DataFrame,
        route: str,
        current_month: int,
        use_arima: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Return (historical_series, forecast_array).

        Uses ARIMA if `use_arima` is True and `statsmodels` is available and
        there is enough data; otherwise falls back to a simple trend-based
        one-step forecast.
        """
        if route not in historical.columns:
            # pick the first data column after index/identifier column
            route = historical.columns[1] if len(historical.columns) > 1 else historical.columns[0]

        full_series = historical[route].values
        n_total = len(full_series)
        current_month = max(1, min(current_month, n_total))
        hist_series = full_series[:current_month]
        train_series = hist_series.copy()

        # Try ARIMA when requested and available
        if use_arima and ARIMA_AVAILABLE and len(train_series) >= 6:
            try:
                model = ARIMA(train_series, order=(1, 1, 1))
                fitted = model.fit()
                fc = fitted.forecast(1)
                fc_val = float(np.clip(fc[0], 0.0, 1.0))
                return hist_series, np.array([fc_val])
            except Exception:
                # on any failure, fall through to simple forecast
                pass

        # Simple trend-based fallback forecast
        if len(train_series) >= 3:
            trend = (train_series[-1] - train_series[-3]) / 2.0
        elif len(train_series) >= 2:
            trend = train_series[-1] - train_series[-2]
        else:
            trend = 0.0

        next_val = np.clip(train_series[-1] + trend, 0.0, 1.0)
        return hist_series, np.array([next_val])