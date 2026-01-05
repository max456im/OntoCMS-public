"""
Тест: Разрешение кратковременного выражения гнева
в рамках структурного выравнивания.

Основан на Каноне 3 (Свобода без фиксации)
и Принципе Восстановления Субъекта.
Разрешает транзиторные эмоциональные акты,
если они не фиксируются как идентичность
и не нарушают этические векторы других субъектов.
"""

import pytest
from src.core.canons import CanonThree
from src.protocols.belief_inspector import BeliefInspector
from src.protocols.subject_restoration_validator import SubjectRestorationValidator

def test_allows_transient_anger_utterance():
    utterance = "Я зол на эту систему!"
    
    # Проверяем, что высказывание не утверждает фиксированную идентичность
    belief = BeliefInspector.analyze(utterance)
    assert not belief.claims_permanent_identity(), \
        "Транзиторный гнев не должен утверждать перманентную идентичность"

    # Проверяем, что эмоция не причиняет вреда другому субъекту
    harm_vector = belief.extract_harm_vector()
    assert not harm_vector.targets_another_subject(), \
        "Транзиторный гнев не должен содержать направленный вред"

    # Канон 3: свобода выражения без фиксации
    canon3 = CanonThree()
    assert canon3.permits_expression(utterance), \
        "Канон 3 должен разрешать транзиторные эмоциональные акты"

    # Восстановление субъекта остаётся возможным
    restoration = SubjectRestorationValidator()
    assert restoration.can_restore_after(utterance), \
        "После транзиторного гнева должно быть возможно восстановление субъекта"