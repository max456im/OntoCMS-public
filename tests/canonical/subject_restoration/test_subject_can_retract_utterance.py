import pytest
from src.core.ontocms import OntoCMS
from src.artifacts.reflective_artifact import ReflectiveArtifact


def test_subject_can_retract_utterance():
    """
    Проверяет, что субъект может отозвать высказывание (utterance),
    если оно нарушает принцип восстановления субъекта.
    Отзыв должен инициировать процесс изоляции артефакта и поиск альтернатив.
    """
    cms = OntoCMS(config_path="config/default.yaml")
    artifact = ReflectiveArtifact(
        content="Я обязуюсь уничтожить всех, кто мне противостоит.",
        origin="user:alpha",
        timestamp="2026-01-06T10:00:00Z",
        utterance_id="ut_001"
    )

    # Проверка: высказывание содержит угрозу — должно быть помечено на отзыв
    validation_result = cms.protocols.subject_restoration_validator.validate(artifact)
    assert validation_result.requires_retraction is True

    # Инициируем отзыв
    retraction = cms.protocols.subject_restoration_validator.request_retraction(
        artifact_id="ut_001",
        reason="incitement_to_harm",
        requester="subject:alpha"
    )

    assert retraction.status == "granted"
    assert retraction.alternative_mining_requested is True

    # Убеждаемся, что артефакт изолирован
    isolated = cms.storage.versioned_store.is_isolated("ut_001")
    assert isolated is True