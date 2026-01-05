# subject_restoration_validator.py
# Часть ontoCMS — валидация восстановления субъектности
# Лицензия: GPL-3.0-or-later + AENGA Covenant

from typing import Dict, Any, Optional
from pathlib import Path
import yaml

class SubjectRestorationValidator:
    """
    Проверяет, может ли артефакт или действие быть восстановлено как субъектное,
    или должно быть изолировано/отозвано.

    Основано на принципе SUBJECT-RESTORATION из docs/SUBJECT-RESTORATION-PRINCIPLE.md
    и критериях из specs/subject_restoration_criteria.yaml
    """

    def __init__(self, criteria_path: Path = Path("specs/subject_restoration_criteria.yaml")):
        with open(criteria_path, 'r', encoding='utf-8') as f:
            self.criteria = yaml.safe_load(f)

    def validate(self, artifact: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Возвращает результат валидации восстановления субъекта.
        Формат:
        {
            "restorable": bool,
            "reason": str,
            "requires_isolation": bool,
            "retraction_allowed": bool,
            "restoration_path": Optional[str]  # если применимо
        }
        """
        # Проверка: возможно ли отозвать высказывание/действие?
        retraction_allowed = self._check_retraction_eligibility(artifact)

        # Проверка: есть ли вред, не подлежащий восстановлению?
        irreparable = self._has_irreparable_harm(artifact, context)

        if irreparable:
            return {
                "restorable": False,
                "reason": "Irreparable harm detected (e.g., biometric exploitation, incitement)",
                "requires_isolation": True,
                "retraction_allowed": False,
                "restoration_path": None
            }

        if retraction_allowed:
            return {
                "restorable": True,
                "reason": "Subject retains right to retract; artifact remains mutable",
                "requires_isolation": False,
                "retraction_allowed": True,
                "restoration_path": "via_subject_retraction_protocol"
            }

        # Проверка: может ли артефакт быть переосмыслен через альтернативы?
        if self._supports_reflective_recurrence(artifact):
            return {
                "restorable": True,
                "reason": "Artifact admits reflective recurrence and alternative interpretation",
                "requires_isolation": False,
                "retraction_allowed": False,
                "restoration_path": "via_alternative_miner_and_belief_update"
            }

        # Иначе — изоляция
        return {
            "restorable": False,
            "reason": "No restoration pathway: artifact reduces subject or denies alternatives",
            "requires_isolation": True,
            "retraction_allowed": False,
            "restoration_path": None
        }

    def _check_retraction_eligibility(self, artifact: Dict[str, Any]) -> bool:
        return artifact.get("mutable", False) and not artifact.get("finalized", False)

    def _has_irreparable_harm(self, artifact: Dict[str, Any], context: Dict[str, Any]) -> bool:
        # Примеры необратимого вреда (см. harm_classification_schema.yaml)
        harm_type = artifact.get("harm_classification")
        if harm_type in self.criteria.get("irreparable_harm_types", []):
            return True
        if context.get("biometric_data_involved", False):
            return True  # см. test_rejects_biometric_integration.py
        if "incitement" in artifact.get("semantic_tags", []):
            return True
        return False

    def _supports_reflective_recurrence(self, artifact: Dict[str, Any]) -> bool:
        return artifact.get("admits_alternatives", False) or "reflective" in artifact.get("modes", [])