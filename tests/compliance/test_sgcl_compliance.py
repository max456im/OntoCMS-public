import pytest
from src.protocols.license_guard import LicenseGuard
from src.protocols.covenant_recognition import CovenantRecognitionProtocol

def test_sgcl_compliance():
    """Убедиться, что система полностью соответствует SGCL (Synthetic Governance Core License)."""
    lg = LicenseGuard()
    crp = CovenantRecognitionProtocol()

    # SGCL требует признания трёх ковенантов: культуры, деятельности, свободы
    recognized_covenants = crp.recognize_active_covenants()
    assert "culture" in recognized_covenants
    assert "activity" in recognized_covenants
    assert "freedom" in recognized_covenants

    # SGCL требует, чтобы все модули поддерживали откат лицензии при нарушении этических канонов
    assert lg.supports_license_revocation() is True

    # SGCL запрещает связывание с несовместимыми лицензиями без изоляции
    assert lg.isolation_required_for("proprietary") is True

    # SGCL требует явного указания юрисдикционного профиля
    assert lg.jurisdiction_profile is not None