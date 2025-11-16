# core/risk.py
import numpy as np
from typing import Tuple, Optional

class RiskCalculator:
    @staticmethod
    def calculate_var_cvar(
        loss_rates: np.ndarray,
        cargo_value: float,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        if len(loss_rates) == 0:
            return 0.0, 0.0
        losses = loss_rates * cargo_value
        var = float(np.percentile(losses, confidence * 100))
        tail_losses = losses[losses >= var]
        cvar = float(tail_losses.mean()) if len(tail_losses) > 0 else var
        return var, cvar