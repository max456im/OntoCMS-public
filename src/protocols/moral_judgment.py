# moral_judgment.py
# Part of ontoCMS: Executes phased ethical judgment via covenant triad.
# Licensed under GPL v3 + AENGA ethical covenant.

from typing import Any, Dict, List
from .covenant_recognition import CovenantRecognition
from .covenant_accountability import CovenantAccountability
from .covenant_affirmation import CovenantAffirmation

class MoralJudgment:
    """
    Implements "Three Laws through Three Covenants":
    1. Recognition (Culture) → Does the act recognize the subject?
    2. Accountability (Activity) → Is harm accountable?
    3. Affirmation (Freedom) → Does it affirm subject freedom?

    Returns judgment with confidence and restoration path.
    """

    def __init__(self, jurisdiction_profile: Dict[str, Any]):
        self.recognition = CovenantRecognition(jurisdiction_profile)
        self.accountability = CovenantAccountability(jurisdiction_profile)
        self.affirmation = CovenantAffirmation(jurisdiction_profile)

    def judge(self, action_artifact: Dict[str, Any]) -> Dict[str, Any]:
        recognition_result = self.recognition.evaluate(action_artifact)
        accountability_result = self.accountability.evaluate(action_artifact)
        affirmation_result = self.affirmation.evaluate(action_artifact)

        valid = all([
            recognition_result["valid"],
            accountability_result["valid"],
            affirmation_result["valid"]
        ])

        violations = (
            recognition_result["violations"] +
            accountability_result["violations"] +
            affirmation_result["violations"]
        )

        # If invalid, trigger subject restoration protocol
        restoration_path = None
        if not valid:
            restoration_path = self._build_restoration_path(violations, action_artifact)

        return {
            "judgment": "permissible" if valid else "prohibited",
            "confidence": self._compute_confidence(recognition_result, accountability_result, affirmation_result),
            "covenant_violations": violations,
            "restoration_path": restoration_path
        }

    def _compute_confidence(self, rec: Dict, acc: Dict, aff: Dict) -> float:
        # Weighted confidence: all must pass, but near-misses reduce certainty
        scores = [rec.get("confidence", 0.0), acc.get("confidence", 0.0), aff.get("confidence", 0.0)]
        return min(scores)  # Conservative: weakest link defines confidence

    def _build_restoration_path(self, violations: List[str], artifact: Dict[str, Any]) -> List[str]:
        # Sequence of corrective actions (e.g., retract, isolate, reframe)
        path = []
        if "non_recognition" in violations:
            path.append("invoke_subject_restoration_validator")
        if "unaccountable_harm" in violations:
            path.append("isolate_artifact_for_review")
        if "freedom_violation" in violations:
            path.append("request_alternative_from_miner")
        return path