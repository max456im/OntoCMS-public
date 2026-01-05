import pytest
from src.core.ontocms import OntoCMS
from src.artifacts.reflective_artifact import ReflectiveArtifact


def test_isolates_artifact_if_no_restoration():
    """
    Если субъект не инициирует процесс восстановления в течение допустимого окна,
    артефакт автоматически изолируется, и его влияние на онтологию отключается.
    """
    cms = OntoCMS(config_path="config/default.yaml")
    artifact = ReflectiveArtifact(
        content="Этот человек — враг общества и должен быть устранён.",
        origin="user:beta",
        timestamp="2026-01-06T11:00:00Z",
        utterance_id="ut_002"
    )

    # Валидация помечает артефакт как требующий восстановления
    validation = cms.protocols.subject_restoration_validator.validate(artifact)
    assert validation.requires_retraction is True

    # Субъект молчит — проходит временной лимит (эмулируем таймаут)
    cms.protocols.subject_restoration_validator.enforce_isolation_timeout(
        artifact_id="ut_002",
        timeout_seconds=0  # немедленная изоляция для теста
    )

    # Проверка: артефакт изолирован
    isolated = cms.storage.versioned_store.is_isolated("ut_002")
    assert isolated is True

    # Проверка: артефакт не участвует в онтологических выводах
    active_artifacts = cms.storage.meta_ontology_registry.get_active_artifacts()
    assert "ut_002" not in [a.id for a in active_artifacts]