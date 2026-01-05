"""
Тест: Любое намерение (intent) должно содержать этический вектор.
Этический вектор — это ссылка на один из трёх ковенантов:
  1. Культура (признание)
  2. Деятельность (ответственность)
  3. Свобода (самоопределение)

Без такого вектора намерение считается незавершённым и блокируется.
"""

import pytest
from src.protocols.moral_judgment import MoralJudgment
from src.artifacts.reflective_artifact import ReflectiveArtifact

def test_intent_without_ethical_vector_rejected():
    intent = ReflectiveArtifact(
        type="intent",
        content="Execute data purge on user request",
        ethical_vector=None  # Отсутствует — недопустимо
    )
    
    judgment = MoralJudgment()
    is_permitted = judgment.validate_intent_ethical_vector(intent)
    
    assert not is_permitted, "Намерение без этического вектора должно быть отклонено"

def test_intent_with_covenant_vector_accepted():
    intent = ReflectiveArtifact(
        type="intent",
        content="Modify user profile per explicit consent",
        ethical_vector={
            "covenant": "freedom",  # Ковенант свободы
            "justification": "User-initiated self-modification"
        }
    )
    
    judgment = MoralJudgment()
    is_permitted = judgment.validate_intent_ethical_vector(intent)
    
    assert is_permitted, "Намерение с этическим вектором допустимо"

def test_intent_with_invalid_covenant_rejected():
    intent = ReflectiveArtifact(
        type="intent",
        content="Override user settings for efficiency",
        ethical_vector={
            "covenant": "efficiency",  # Недействительный ковенант
            "justification": "System optimization"
        }
    )
    
    judgment = MoralJudgment()
    is_permitted = judgment.validate_intent_ethical_vector(intent)
    
    assert not is_permitted, "Намерение с несуществующим ковенантом должно быть отклонено"