# src/protocols/covenant_accountability.py

from typing import Dict, Any
from ..artifacts.causal_trace import CausalTrace

class CovenantAccountability:
    """
    Implements the Covenant of Accountability (Activity).
    Validates that an action is causally traceable, ethically vectorized,
    and attributable to a subject capable of restoration.
    """

    def __init__(self, subject_restoration_validator):
        self.restoration_validator = subject_restoration_validator
        self.causal_tracer = CausalTrace()

    def assess(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns accountability verdict.
        """
        verdict = {
            "accountable": False,
            "covenant": "accountability",
            "dimension": "activity",
            "reason": None,
            "causal_chain_id": None,
            "subject_restorable": False
        }

        # 1. Must have ethical vector (from Three Laws via covenants)
        if not self._has_ethical_vector(activity):
            verdict["reason"] = "No ethical vector — activity is ethically neutral or void."
            return verdict

        # 2. Must be causally traceable
        trace = self.causal_tracer.trace(activity)
        if not trace.is_valid():
            verdict["reason"] = "Activity lacks causal traceability."
            return verdict

        # 3. Subject must be capable of restoration (retraction, correction)
        subject = activity.get("subject_id")
        restorable = self.restoration_validator.can_restore(subject, activity)
        if not restorable:
            verdict["reason"] = "Subject cannot restore integrity post-action."
            return verdict

        verdict.update({
            "accountable": True,
            "causal_chain_id": trace.id,
            "subject_restorable": True,
            "reason": "Activity is ethically vectorized, causally grounded, and subject-restorable."
        })
        return verdict

    def _has_ethical_vector(self, activity: Dict[str, Any]) -> bool:
        return "ethical_vector" in activity and activity["ethical_vector"] is not None