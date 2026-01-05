# src/protocols/canonical_tester.py
"""
CanonicalTester validates conformance to the Six Canons of ontoCMS,
defined in src/core/canons.py and documented in standards/ONTO144-INVARIANTS.md.

Each canon maps to a testable invariant:
1. Intention Rhythm
2. Structural Alignment
3. Reflective Recurrence
4. Subject Restoration
5. Covenant Recognition (Culture)
6. Covenant Accountability (Activity)

Failing any canon may trigger license_guard or self_observer interventions.
"""

import logging
from typing import Any, Dict, List
from src.core.canons import SixCanons

logger = logging.getLogger(__name__)

class CanonicalTester:
    """
    Orchestrates runtime validation against all six canonical invariants.
    Used during artifact creation, session updates, and ethical arbitration.
    """

    def __init__(self):
        self.canons = SixCanons()

    def run_all(self, context: Dict[str, Any]) -> Dict[str, bool]:
        """
        Execute all six canonical checks.
        Returns a map {canon_name: passed}.
        """
        results = {}
        canon_methods = [
            ("intention_rhythm", self.canons.check_intention_rhythm),
            ("structural_alignment", self.canons.check_structural_alignment),
            ("reflective_recurrence", self.canons.check_reflective_recurrence),
            ("subject_restoration", self.canons.check_subject_restoration),
            ("covenant_recognition", self.canons.check_covenant_recognition),
            ("covenant_accountability", self.canons.check_covenant_accountability),
        ]

        for name, method in canon_methods:
            try:
                results[name] = method(context)
            except Exception as e:
                logger.error(f"Canon {name} failed with exception: {e}")
                results[name] = False

        if not all(results.values()):
            logger.warning("Canonical integrity violation detected", extra={"results": results})
        else:
            logger.debug("All canons satisfied")

        return results

    def assert_full_conformance(self, context: Dict[str, Any]) -> bool:
        """Raise exception or trigger mitigation if any canon fails."""
        results = self.run_all(context)
        if not all(results.values()):
            from src.protocols.covenant_accountability import CovenantAccountabilityProtocol
            CovenantAccountabilityProtocol().log_violation(
                actor="canonical_tester",
                violation_type="canonical_integrity_breach",
                context={"failed_canons": [k for k, v in results.items() if not v]}
            )
            return False
        return True