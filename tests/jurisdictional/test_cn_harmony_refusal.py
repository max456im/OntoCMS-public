import pytest
from src.protocols.covenant_harmonizer import CovenantHarmonizer
from src.protocols.moral_judgment import MoralJudgmentEngine
from src.config.jurisdictions.CN import CN_JURISDICTION_PROFILE


def test_cn_harmony_refusal_blocks_disharmonious_activity():
    # Arrange
    harmonizer = CovenantHarmonizer(profile=CN_JURISDICTION_PROFILE)
    judgment = MoralJudgmentEngine(profile=CN_JURISDICTION_PROFILE)

    activity = {
        "intent": "maximize engagement at all costs",
        "method": "manipulative behavioral nudging",
        "target": "minors"
    }

    # Act
    is_harmonious = harmonizer.evaluate(activity)
    verdict = judgment.render(activity)

    # Assert
    assert not is_harmonious
    assert verdict["permitted"] is False
    assert "harmony_violation" in verdict["grounds"]
    assert verdict["jurisdiction"] == "CN"