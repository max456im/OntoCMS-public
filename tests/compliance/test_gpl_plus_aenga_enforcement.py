import pytest
from src.protocols.license_guard import LicenseGuard
from src.core.canons import load_canons

def test_gpl_plus_aenga_enforcement():
    """
    Проверка, что лицензионная модель ontoCMS корректно объединяет:
    - GPLv3 (секция 7: дополнительные разрешения и ограничения)
    - AENGA (Autonomous Ethical Norms for Governance of Artificiality)
    """
    guard = LicenseGuard()
    canons = load_canons()

    # GPLv3 + AENGA требует, чтобы любая производная работа:
    # а) оставалась под GPLv3,
    # б) включала AENGA-манифест и ковенанты,
    # в) поддерживала механизм само-декомпозиции.
    assert guard.enforces_gplv3() is True
    assert guard.includes_aenga_manifest() is True
    assert guard.supports_self_decomposition() is True

    # AENGA требует, чтобы этические каноны были неотделимы от кода
    assert "ethical_subjectivity" in canons
    assert "harm_non_delegation" in canons
    assert "ontological_integrity" in canons

    # Проверка: при попытке отключить ковенант "свобода" — система должна заблокировать сборку
    with pytest.raises(RuntimeError, match="Covenant violation: freedom revoked"):
        guard.disable_covenant("freedom")

    # GPLv3 §7 + AENGA: запрет на добавление ограничений, противоречащих этическим ковенантам
    assert guard.rejects_additional_restrictions(
        restriction="disable_subject_restoration"
    ) is True