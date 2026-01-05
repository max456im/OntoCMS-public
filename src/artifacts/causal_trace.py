# SPDX-License-Identifier: GPL-3.0-or-later WITH AENGA-exception
# © 2026 ontoCMS Contributors

"""
CausalTrace — неизменяемая цепочка артефактов и действий,
фиксирующая причинно-следственную последовательность,
включая этические оценки и реакции субъекта.

Используется для:
- детекции вреда,
- валидации восстановления субъектности,
- аудита решений этического арбитра.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from src.artifacts.reflective_artifact import ReflectiveArtifact


class CausalTrace:
    """
    Цепочка причинности в онтологическом формате.
    Каждый шаг — это артефакт или действие субъекта.
    """

    def __init__(
        self,
        subject_id: str,
        trace_id: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        initiated_at: Optional[datetime] = None,
        juris_profile: Optional[str] = None,  # e.g., "CN", "ZA"
    ):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.subject_id = subject_id
        self.steps: List[Dict[str, Any]] = steps or []
        self.initiated_at = initiated_at or datetime.now(timezone.utc)
        self.juris_profile = juris_profile
        self.closed = False
        self.closed_at: Optional[datetime] = None

    def add_step(self, artifact: ReflectiveArtifact):
        """Добавляет артефакт как шаг в цепочку причинности."""
        if self.closed:
            raise ValueError("Cannot add step to closed CausalTrace")
        self.steps.append({
            "type": "reflective_artifact",
            "artifact_id": artifact.artifact_id,
            "ethical_vector": artifact.ethical_vector,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "retracted": artifact.retracted,
        })

    def close(self):
        """Завершает цепочку — фиксирует итоговое состояние."""
        if self.closed:
            return
        self.closed = True
        self.closed_at = datetime.now(timezone.utc)

    def contains_harm_indicator(self, harm_classifier) -> bool:
        """Проверяет наличие признаков вреда по внешнему классификатору."""
        for step in self.steps:
            if step["retracted"]:
                continue
            # Предполагается, что harm_classifier принимает ethical_vector
            if harm_classifier.detects_harm(step["ethical_vector"]):
                return True
        return False

    def requires_subject_restoration(self) -> bool:
        """Определяет, требуется ли восстановление субъекта (согласно онтологии)."""
        # Пример условия: если есть неретрагированный артефакт без being
        for step in self.steps:
            if not step.get("retracted") and not step.get("being"):
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "subject_id": self.subject_id,
            "steps": self.steps,
            "initiated_at": self.initiated_at.isoformat(),
            "closed": self.closed,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "juris_profile": self.juris_profile,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        initiated_at = datetime.fromisoformat(data["initiated_at"].replace("Z", "+00:00"))
        closed_at = (
            datetime.fromisoformat(data["closed_at"].replace("Z", "+00:00"))
            if data.get("closed_at")
            else None
        )
        return cls(
            subject_id=data["subject_id"],
            trace_id=data["trace_id"],
            steps=data["steps"],
            initiated_at=initiated_at,
            juris_profile=data.get("juris_profile"),
        )