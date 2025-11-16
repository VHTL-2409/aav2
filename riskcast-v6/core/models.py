from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

class CriterionType(Enum):
    COST = "cost"
    BENEFIT = "benefit"

@dataclass
class AnalysisParams:
    cargo_value: float
    good_type: str = ""
    route: str = "VN - EU"
    method: str = "Sea"
    month: int = 9
    priority_profile: str = "💰 Tiết kiệm chi phí"
    use_fuzzy: bool = True
    use_arima: bool = True
    use_mc: bool = True
    use_var: bool = True
    mc_runs: int = 2000
    fuzzy_uncertainty: float = 15.0

@dataclass
class AnalysisResult:
    results: pd.DataFrame
    weights: pd.Series
    data_adjusted: Optional[pd.DataFrame] = None
    var: Optional[float] = None
    cvar: Optional[float] = None
    historical: Optional[np.ndarray] = None
    forecast: Optional[np.ndarray] = None