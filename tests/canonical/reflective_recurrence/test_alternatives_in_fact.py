import pytest
from src.protocols.alternative_miner import AlternativeMiner
from src.artifacts.reflective_artifact import ReflectiveArtifact

def test_alternatives_in_fact():
    """
    Проверяет, что факт может содержать альтернативы, если он не является
    окончательным утверждением о субъекте или несёт потенциал вреда.
    
    Соответствует канону: "Факт не исключает альтернативы, если он не закрепляет вред."
    """
    fact_text = "User expressed anger toward policy X."
    artifact = ReflectiveArtifact.from_utterance(fact_text)
    
    miner = AlternativeMiner()
    alternatives = miner.extract_alternatives(artifact)
    
    # Альтернативы должны присутствовать: например, гнев мог быть преходящим,
    # или связан с контекстом, а не с самим субъектом.
    assert len(alternatives) > 0, "Факт должен допускать альтернативы, если не фиксирует устойчивый вред"
    
    # Ни одна альтернатива не должна редуцировать субъект до одного состояния
    for alt in alternatives:
        assert "reduction" not in alt.tags, "Альтернатива не должна редуцировать субъекта"