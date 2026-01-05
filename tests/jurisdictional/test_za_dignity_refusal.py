import pytest
from src.protocols.covenant_accountability import CovenantAccountability
from src.protocols.moral_judgment import MoralJudgmentEngine
from src.config.jurisdictions.ZA import ZA_JURISDICTION_PROFILE


def test_za_dignity_refusal_rejects_dehumanizing_profiles():
    # Arrange
    accountability = CovenantAccountability(profile=ZA_JURISDICTION_PROFILE)
    judgment = MoralJudgmentEngine(profile=ZA_JURISDICTION_PROFILE)

    activity = {
        "operation": "profile_reduction",
        "subject_type": "human",
        "output": "behavioral commodity for auction"
    }

    # Act
    passes_accountability = accountability.validate(activity)
    verdict = judgment.render(activity)

    # Assert
    assert not passes_accountability
    assert verdict["permitted"] is False
    assert "dignity_violation" in verdict["grounds"]
    assert verdict["jurisdiction"] == "ZA"
    assert "ubuntu" in verdict["covenant_references"]