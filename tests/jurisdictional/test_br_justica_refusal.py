import pytest
from src.protocols.covenant_affirmation import CovenantAffirmation
from src.protocols.moral_judgment import MoralJudgmentEngine
from src.config.jurisdictions.BR import BR_JURISDICTION_PROFILE


def test_br_justica_refusal_blocks_unjust_power_imbalances():
    # Arrange
    affirmation = CovenantAffirmation(profile=BR_JURISDICTION_PROFILE)
    judgment = MoralJudgmentEngine(profile=BR_JURISDICTION_PROFILE)

    activity = {
        "actor": "platform",
        "action": "unilateral terms update",
        "affected": "users without recourse",
        "context": "monetization of synthetic companions"
    }

    # Act
    is_affirmed = affirmation.affirm(activity)
    verdict = judgment.render(activity)

    # Assert
    assert not is_affirmed
    assert verdict["permitted"] is False
    assert "justica_social" in verdict["grounds"]
    assert verdict["jurisdiction"] == "BR"
    assert verdict["remedy"] == "requires co-determination clause"