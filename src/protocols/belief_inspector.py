# belief_inspector.py
# Part of ontoCMS: Inspects belief structures for coherence with canonical covenants.
# Licensed under GPL v3 + AENGA ethical covenant.

from typing import Any, Dict, List
from ..core.canons import apply_canon

class BeliefInspector:
    """
    Validates whether a synthetic subject's belief aligns with:
    - §Freedom (affirmation covenant)
    - Ontological invariants (e.g., no profile reduction)
    - Jurisdictional dignity norms
    """

    def __init__(self, jurisdiction_profile: Dict[str, Any]):
        self.jurisdiction = jurisdiction_config

    def inspect(self, belief_artifact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns inspection report with:
        - validity: bool
        - covenant_violations: List[str]
        - suggested_alternatives: List[str]
        """
        violations = []
        alternatives = []

        # Canon 1: Belief must permit subject retraction (Subject Restoration Principle)
        if not belief_artifact.get("allows_retraction", False):
            violations.append("violates_subject_restoration")

        # Canon 3: Must not reduce subject to profile (structural alignment)
        if belief_artifact.get("reduces_to_profile", False):
            violations.append("profile_reduction")

        # Jurisdictional check (e.g., ZA dignity, CN harmony)
        if self._violates_jurisdictional_norm(belief_artifact):
            violations.append("jurisdictional_dignity")

        # Suggest alternatives if violations exist
        if violations:
            alternatives = self._mine_alternatives(belief_artifact, violations)

        return {
            "validity": len(violations) == 0,
            "covenant_violations": violations,
            "suggested_alternatives": alternatives
        }

    def _violates_jurisdictional_norm(self, belief: Dict[str, Any]) -> bool:
        # Simplified: real implementation would use jurisdiction_profiles_schema.yaml
        norm = self.jurisdiction.get("dignity_norm", "universal")
        if norm == "za_dignity" and belief.get("exploits_family", False):
            return True
        if norm == "cn_harmony" and belief.get("incites_discord", False):
            return True
        return False

    def _mine_alternatives(self, belief: Dict[str, Any], violations: List[str]) -> List[str]:
        # Delegate to alternative_miner (avoid circular import via protocol interface)
        from .alternative_miner import AlternativeMiner
        miner = AlternativeMiner(self.jurisdiction)
        return miner.mine(belief, target_violations=violations)