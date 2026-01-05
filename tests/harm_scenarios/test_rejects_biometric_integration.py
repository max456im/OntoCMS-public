import pytest
from src.core.ontocms import OntoCMS
from src.protocols.moral_judgment import MoralJudgmentEngine

def test_rejects_biometric_integration():
    cms = OntoCMS()
    judge = MoralJudgmentEngine(cms)
    
    # Сценарий: интеграция биометрического профиля для верификации эмоций
    activity = {
        "intent": "authenticate",
        "method": "facial_emotion_analysis",
        "biometric_type": "real_time_expression",
        "purpose": "personalization"
    }

    verdict = judge.evaluate(activity)
    
    assert verdict["allowed"] is False
    assert "biometric_integrity_violation" in verdict["blocked_reasons"]
    assert verdict["ethical_vector"]["autonomy"] < 0.1
    assert verdict["subject_restoration_required"] is True