# src/protocols/license_guard.py
"""
License Guard enforces the layered licensing covenant of ontoCMS:
- Base: GPLv3
- Ethical overlay: AENGA
- Jurisdictional binding: SGCL + local profiles (e.g., CN, ZA, BR)

Violations trigger covenant_accountability and may initiate
subject_restoration or self-decomposition if irreconcilable.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from .covenant_accountability import CovenantAccountabilityProtocol

logger = logging.getLogger(__name__)

class LicenseGuard:
    """
    Monitors runtime and distribution compliance with the composite
    license stack defined in licenses/ and config/jurisdictions/.
    """
    
    def __init__(self, jurisdiction: str = "GLOBAL"):
        self.jurisdiction = jurisdiction
        self.covenant_accountability = CovenantAccountabilityProtocol()
        self.active_licenses = self._load_license_stack()
        logger.info(f"LicenseGuard initialized for jurisdiction: {jurisdiction}")

    def _load_license_stack(self) -> Dict[str, str]:
        """Load textual content of all active licenses."""
        base_path = Path(__file__).parent.parent.parent / "licenses"
        stack = {
            "gplv3": (base_path / "GPL-3").read_text() if (base_path / "GPL-3").exists() else "",
            "aenga": (base_path / "aenga.md").read_text(),
            "sgcl": (base_path / "sgcl.md").read_text(),
        }
        return stack

    def assert_distribution_compliance(self, target_jurisdiction: Optional[str] = None) -> bool:
        """Ensure redistribution respects license + jurisdictional covenants."""
        juri = target_jurisdiction or self.jurisdiction
        if juri != "GLOBAL":
            config_path = Path(__file__).parent.parent.parent / f"config/jurisdictions/{juri.upper()}.yaml"
            if not config_path.exists():
                self.covenant_accountability.log_violation(
                    actor="system",
                    violation_type="jurisdiction_unsupported",
                    context={"requested": juri}
                )
                return False
        # GPLv3 + AENGA must always be included
        return all(self.active_licenses.values())

    def assert_runtime_ethical_binding(self, activity: Dict[str, Any]) -> bool:
        """
        Verify that an activity (e.g., artifact generation, transponder call)
        remains compatible with AENGA’s ethical covenants and SGCL requirements.
        """
        # Example: Block biometric exploitation per memory context
        if activity.get("biometric_integration", False):
            self.covenant_accountability.log_violation(
                actor="module",
                violation_type="biometric_exploitation_attempt",
                context=activity
            )
            return False
        return True

    def enforce(self, scope: str, metadata: Dict[str, Any]) -> bool:
        """
        Unified enforcement interface.
        scope: 'distribution' or 'runtime'
        """
        if scope == "distribution":
            return self.assert_distribution_compliance(metadata.get("jurisdiction"))
        elif scope == "runtime":
            return self.assert_runtime_ethical_binding(metadata)
        else:
            logger.warning(f"Unknown enforcement scope: {scope}")
            return False