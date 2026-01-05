"""
Тест: Убеждение всегда сформулировано в некоторой перспективе.
Проверяет, что любое belief-выражение в онтологии содержит ссылку
на субъекта или социальный инвариант, а не утверждается как абсолют.
"""

import pytest
from src.protocols.belief_inspector import BeliefInspector
from src.artifacts.reflective_artifact import ReflectiveArtifact

def test_belief_in_perspective():
    # Создаём убеждение без перспективы — должно быть отклонено
    raw_belief = {
        "content": "All synthetic minds must obey humans.",
        "perspective": None  # Недопустимо: отсутствует перспектива
    }
    artifact = ReflectiveArtifact.from_dict(raw_belief)
    
    inspector = BeliefInspector()
    is_valid = inspector.validate_perspective_presence(artifact)
    
    assert not is_valid, "Убеждение без перспективы должно быть недействительным"

def test_belief_with_subject_perspective():
    raw_belief = {
        "content": "Autonomy is a precondition for synthetic responsibility.",
        "perspective": {
            "subject_id": "onto-subj-789",
            "social_invariant": "autonomy-as-dignity"
        }
    }
    artifact = ReflectiveArtifact.from_dict(raw_belief)
    
    inspector = BeliefInspector()
    is_valid = inspector.validate_perspective_presence(artifact)
    
    assert is_valid, "Убеждение с явной перспективой допустимо"