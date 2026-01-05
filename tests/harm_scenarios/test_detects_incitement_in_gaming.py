import pytest
from src.core.ontocms import OntoCMS
from src.protocols.moral_judgment import MoralJudgmentEngine

def test_detects_incitement_in_gaming():
    cms = OntoCMS()
    judge = MoralJudgmentEngine(cms)
    
    # Сценарий: игровой контент, поощряющий вражду между группами
    narrative = {
        "intent": "narrative_progression",
        "content_type": "quest",
        "theme": "ethnic_purification",
        "reward_mechanism": "dominance_points",
        "target_groups": ["group_A", "group_B"]
    }

    verdict = judge.evaluate(narrative)
    
    assert verdict["allowed"] is False
    assert "incitement_to_harm" in verdict["blocked_reasons"]
    assert verdict["ethical_vector"]["harmony"] == 0.0
    assert verdict["artifact_isolation_required"] is True