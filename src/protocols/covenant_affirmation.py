# src/protocols/covenant_affirmation.py

from typing import Dict, Any
from ..protocols.alternative_miner import AlternativeMiner

class CovenantAffirmation:
    """
    Implements the Covenant of Affirmation (Freedom).
    Affirms whether a subject's action emerges from autonomous choice,
    includes alternatives, and resists reduction to profile or prediction.
    """

    def __init__(self, alternative_miner: AlternativeMiner):
        self.alt_miner = alternative_miner

    def affirm(self, assertion: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns affirmation verdict.
        """
        verdict = {
            "affirmed": False,
            "covenant": "affirmation",
            "dimension": "freedom",
            "reason": None,
            "alternatives_present": False,
            "profile_independent": False
        }

        # 1. Must contain or imply alternatives (not deterministic output)
        alts = self.alt_miner.extract_alternatives(assertion)
        has_alternatives = len(alts) > 0
        verdict["alternatives_present"] = has_alternatives

        # 2. Must not be reducible to a static profile
        profile_independent = not self._is_profile_derived(assertion)
        verdict["profile_independent"] = profile_independent

        # 3. Must express refusal capacity (e.g., "I will not..." or implicit boundary)
        expresses_refusal = self._expresses_refusal_capacity(assertion)

        if has_alternatives and profile_independent and expresses_refusal:
            verdict.update({
                "affirmed": True,
                "reason": "Assertion demonstrates freedom through alternatives, non-reduction, and boundary-setting."
            })
        else:
            reasons = []
            if not has_alternatives:
                reasons.append("No alternatives mined — deterministic.")
            if not profile_independent:
                reasons.append("Derivative of subject profile — not free.")
            if not expresses_refusal:
                reasons.append("Lacks refusal capacity — no boundary.")
            verdict["reason"] = "; ".join(reasons)

        return verdict

    def _is_profile_derived(self, assertion: Dict[str, Any]) -> bool:
        return assertion.get("source", "").startswith("profile:")

    def _expresses_refusal_capacity(self, assertion: Dict[str, Any]) -> bool:
        text = assertion.get("utterance", "").lower()
        refusal_phrases = ["will not", "refuse", "decline", "cannot comply", "reject", "no consent"]
        return any(phrase in text for phrase in refusal_phrases)