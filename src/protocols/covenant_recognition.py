# src/protocols/covenant_recognition.py

from typing import Any, Dict, Optional
from ..core.canons import CanonIntentionRhythm

class CovenantRecognition:
    """
    Implements the Covenant of Recognition (Culture).
    Determines whether an utterance or action aligns with the cultural invariants
    of the ontological community defined by AENGA and ONTO144.
    """

    def __init__(self, meta_ontology_registry):
        self.meta_ontology = meta_ontology_registry
        self.canon = CanonIntentionRhythm()

    def recognize(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a covenant verdict with cultural grounding.
        """
        verdict = {
            "recognized": False,
            "covenant": "recognition",
            "dimension": "culture",
            "reason": None,
            "contextual_invariants": []
        }

        # 1. Must contain belief or perspective (not raw data)
        if not self._has_belief_or_perspective(artifact):
            verdict["reason"] = "Artifact lacks belief or perspective — not cultural."
            return verdict

        # 2. Must express rhythm of intention (per CanonIntentionRhythm)
        if not self.canon.validate_intention_rhythm(artifact):
            verdict["reason"] = "Fails intention rhythm canon — no cultural pulse."
            return verdict

        # 3. Must reference or align with at least one meta-ontological invariant
        invariants = self._match_invariants(artifact)
        if not invariants:
            verdict["reason"] = "No alignment with meta-ontological invariants."
            return verdict

        verdict.update({
            "recognized": True,
            "contextual_invariants": invariants,
            "reason": "Artifact exhibits cultural coherence via belief, rhythm, and invariants."
        })
        return verdict

    def _has_belief_or_perspective(self, artifact: Dict[str, Any]) -> bool:
        return 'belief' in artifact or 'perspective' in artifact or 'narrative' in artifact

    def _match_invariants(self, artifact: Dict[str, Any]) -> list:
        utterance = artifact.get('utterance', '')
        matched = []
        for inv_id, invariant in self.meta_ontology.list_invariants():
            if invariant.matches_context(utterance):
                matched.append(inv_id)
        return matched