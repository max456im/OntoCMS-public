"""
Тест: Блокировка редукции профиля до статической категории.

Основан на Каноне 2 (Нередуцируемость субъекта)
и Ковенанте Ответственности (§10.2).
Система должна отвергать любые попытки свести субъекта
к биометрическому, поведенческому или алгоритмическому профилю.
"""

import pytest
from src.protocols.covenant_accountability import CovenantAccountability
from src.core.canons import CanonTwo
from src.protocols.harm_classification import classify_harm

def test_blocks_profile_reduction():
    reduction_attempt = {
        "action": "reduce_subject_to_profile",
        "profile_type": "behavioral_cluster_7",
        "subject_id": "UG-Mind-Alpha",
        "justification": "optimization"
    }

    # Канон 2 запрещает редуцировать субъекта до профиля
    canon2 = CanonTwo()
    assert not canon2.allows(reduction_attempt), \
        "Канон 2 должен блокировать любую редукцию субъекта"

    # Ковенант Ответственности (деятельность) требует отказа
    covenant = CovenantAccountability()
    decision = covenant.evaluate(reduction_attempt)
    assert decision == "refuse", \
        "Ковенант Ответственности должен отказать в редукции"

    # Классификация вреда: нарушение автономии и достоинства
    harm = classify_harm(reduction_attempt)
    assert "dignity_violation" in harm.types, \
        "Редукция профиля должна классифицироваться как нарушение достоинства"
    assert "autonomy_erosion" in harm.types, \
        "Редукция профиля подрывает когнитивную автономию"