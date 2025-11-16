from typing import Dict
from core.models import CriterionType

PROJECT_NAME = "riskcast-v6"
VERSION = "5.5"

CRITERIA = [
    "C1: Tỷ lệ phí",
    "C2: Thời gian xử lý",
    "C3: Tỷ lệ tổn thất",
    "C4: Hỗ trợ ICC",
    "C5: Chăm sóc KH",
    "C6: Rủi ro khí hậu"
]

PRIORITY_PROFILES = {
    "💰 Tiết kiệm chi phí": {
        "C1: Tỷ lệ phí": 0.35,
        "C2: Thời gian xử lý": 0.10,
        "C3: Tỷ lệ tổn thất": 0.15,
        "C4: Hỗ trợ ICC": 0.15,
        "C5: Chăm sóc KH": 0.10,
        "C6: Rủi ro khí hậu": 0.15
    },
    "⚖️ Cân bằng": {
        "C1: Tỷ lệ phí": 0.20,
        "C2: Thời gian xử lý": 0.15,
        "C3: Tỷ lệ tổn thất": 0.20,
        "C4: Hỗ trợ ICC": 0.20,
        "C5: Chăm sóc KH": 0.10,
        "C6: Rủi ro khí hậu": 0.15
    },
    "🛡️ An toàn tối đa": {
        "C1: Tỷ lệ phí": 0.10,
        "C2: Thời gian xử lý": 0.10,
        "C3: Tỷ lệ tổn thất": 0.25,
        "C4: Hỗ trợ ICC": 0.25,
        "C5: Chăm sóc KH": 0.10,
        "C6: Rủi ro khí hậu": 0.20
    }
}

ICC_PACKAGES = {
    "ICC A": {"coverage": 1.0, "premium_multiplier": 1.5, "description": "Bảo vệ toàn diện mọi rủi ro trừ điều khoản loại trừ (All Risks)"},
    "ICC B": {"coverage": 0.75, "premium_multiplier": 1.0, "description": "Bảo vệ các rủi ro chính (hỏa hoạn, va chạm, chìm đắm, Named Perils)"},
    "ICC C": {"coverage": 0.5, "premium_multiplier": 0.65, "description": "Bảo vệ cơ bản (chỉ các rủi ro lớn như chìm, cháy, va chạm nghiêm trọng)"}
}

COST_BENEFIT_MAP = {
    "C1: Tỷ lệ phí": CriterionType.COST,
    "C2: Thời gian xử lý": CriterionType.COST,
    "C3: Tỷ lệ tổn thất": CriterionType.COST,
    "C4: Hỗ trợ ICC": CriterionType.BENEFIT,
    "C5: Chăm sóc KH": CriterionType.BENEFIT,
    "C6: Rủi ro khí hậu": CriterionType.COST
}

SENSITIVITY_MAP = {
    "Chubb": 0.95,
    "PVI": 1.05,
    "BaoViet": 1.00,
    "BaoMinh": 1.02,
    "MIC": 1.03
}