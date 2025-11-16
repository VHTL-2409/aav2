# core/mcdm.py
import pandas as pd
import numpy as np
from typing import Optional
from .simulation import MonteCarloSimulator
from .risk import RiskCalculator
from .forecaster import Forecaster
from .data import DataService
from utils.fuzzy import apply_fuzzy
from config.constants import (
    PRIORITY_PROFILES, ICC_PACKAGES, COST_BENEFIT_MAP, SENSITIVITY_MAP, CRITERIA
)
from core.models import AnalysisParams, AnalysisResult

class TOPSISAnalyzer:
    @staticmethod
    def analyze(data: pd.DataFrame, weights: pd.Series, cost_benefit) -> np.ndarray:
        M = data[list(weights.index)].values.astype(float)
        denom = np.sqrt((M ** 2).sum(axis=0))
        denom[denom == 0] = 1.0
        R = M / denom
        V = R * weights.values
        is_cost = np.array([cost_benefit[c] == "cost" for c in weights.index])
        ideal_best = np.where(is_cost, V.min(axis=0), V.max(axis=0))
        ideal_worst = np.where(is_cost, V.max(axis=0), V.min(axis=0))
        d_plus = np.sqrt(((V - ideal_best) ** 2).sum(axis=1))
        d_minus = np.sqrt(((V - ideal_worst) ** 2).sum(axis=1))
        return d_minus / (d_plus + d_minus + 1e-12)

class MultiPackageAnalyzer:
    def __init__(self):
        self.topsis = TOPSISAnalyzer()
        self.mc = MonteCarloSimulator()
        self.risk = RiskCalculator()
        self.forecaster = Forecaster()
        self.data_service = DataService()

    def run_analysis(self, params: AnalysisParams) -> AnalysisResult:
        # Load historical data internally
        historical = self.data_service.load_historical_data()
        
        profile_weights = PRIORITY_PROFILES[params.priority_profile]
        weights = pd.Series(profile_weights, index=CRITERIA)

        if params.use_fuzzy:
            weights = apply_fuzzy(weights, params.fuzzy_uncertainty)

        company_data = pd.read_csv("data/company_data.csv").set_index("Company")

        base_risk = float(
            historical.loc[historical["month"] == params.month, params.route].iloc[0]
            if params.month in historical["month"].values else 0.4
        )

        mc_mean = mc_std = np.zeros(len(company_data))
        if params.use_mc:
            companies, mc_mean, mc_std = self.mc.simulate(base_risk, SENSITIVITY_MAP, params.mc_runs)
            order = [companies.index(c) for c in company_data.index]
            mc_mean, mc_std = mc_mean[order], mc_std[order]

        all_options = []
        for company in company_data.index:
            for icc_name, icc_data in ICC_PACKAGES.items():
                option = company_data.loc[company].copy()
                base_premium = option["C1: Tỷ lệ phí"]
                option["C1: Tỷ lệ phí"] = base_premium * icc_data["premium_multiplier"]
                option["C4: Hỗ trợ ICC"] = option["C4: Hỗ trợ ICC"] * icc_data["coverage"]

                idx = list(company_data.index).index(company)
                option["C6: Rủi ro khí hậu"] = mc_mean[idx]

                all_options.append({
                    "company": company, "icc_package": icc_name, "coverage": icc_data["coverage"],
                    "premium_rate": option["C1: Tỷ lệ phí"],
                    "estimated_cost": params.cargo_value * option["C1: Tỷ lệ phí"],
                    **{k: option[k] for k in CRITERIA}, "C6_std": mc_std[idx]
                })

        data_adjusted = pd.DataFrame(all_options)
        if params.cargo_value > 50_000:
            data_adjusted["C1: Tỷ lệ phí"] *= 1.1
            data_adjusted["estimated_cost"] *= 1.1

        scores = self.topsis.analyze(
            data_adjusted[CRITERIA], weights, {k: v.value for k, v in COST_BENEFIT_MAP.items()}
        )
        data_adjusted["score"] = scores
        data_adjusted = data_adjusted.sort_values("score", ascending=False).reset_index(drop=True)
        data_adjusted["rank"] = data_adjusted.index + 1

        data_adjusted["category"] = data_adjusted["icc_package"].map({
            "ICC C": "Tiết kiệm", "ICC B": "Cân bằng", "ICC A": "An toàn"
        })

        eps = 1e-9
        cv_c6 = data_adjusted["C6_std"].values / (data_adjusted["C6: Rủi ro khí hậu"].values + eps)
        conf = 1.0 / (1.0 + cv_c6)
        conf = 0.3 + 0.7 * (conf - conf.min()) / (np.ptp(conf) + eps)
        data_adjusted["confidence"] = conf

        var = cvar = None
        if params.use_var:
            var, cvar = self.risk.calculate_var_cvar(data_adjusted["C6: Rủi ro khí hậu"].values, params.cargo_value)

        hist_series, forecast = self.forecaster.forecast(historical, params.route, params.month, params.use_arima)

        return AnalysisResult(
            results=data_adjusted,
            weights=weights,
            data_adjusted=data_adjusted,
            var=var, cvar=cvar,
            historical=hist_series,
            forecast=forecast
        )