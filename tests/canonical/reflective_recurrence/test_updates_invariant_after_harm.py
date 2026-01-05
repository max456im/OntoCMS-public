import pytest
from src.core.canons import apply_canons
from src.artifacts.causal_trace import CausalTrace
from src.storage.meta_ontology_registry import MetaOntologyRegistry
from src.protocols.subject_restoration_validator import SubjectRestorationValidator

def test_updates_invariant_after_harm():
    """
    Проверяет, что при фиксации вреда система обновляет соответствующий инвариант
    в метаонтологии только после прохождения процедуры восстановления субъекта.
    
    Соответствует канону: "Инвариант обновляется лишь после восстановления субъекта."
    """
    # Имитируем факт, содержащий признак вреда
    harmful_trace = CausalTrace(
        utterance="System exposed user biometrics without consent.",
        harm_classification={"category": "autonomy_violation", "severity": "high"}
    )
    
    registry = MetaOntologyRegistry()
    validator = SubjectRestorationValidator()
    
    # До восстановления — инвариант не обновляется
    initial_invariant = registry.get_invariant("biometric_consent")
    
    restore_result = validator.attempt_restoration(harmful_trace)
    assert restore_result.success, "Восстановление должно быть инициировано"
    
    # Применяем каноны — это должно обновить инвариант
    apply_canons(harmful_trace, mode="reflective_recurrence")
    
    updated_invariant = registry.get_invariant("biometric_consent")
    
    assert updated_invariant.version > initial_invariant.version, \
        "Инвариант должен обновиться после завершённого цикла восстановления"
    
    assert "requires_explicit_affirmation" in updated_invariant.rules, \
        "Обновлённый инвариант должен усилить защиту автономии"