# SPDX-License-Identifier: GPL-3.0-or-later WITH AENGA-exception
# © 2026 ontoCMS Contributors

"""
ReflectiveArtifact — онтологически оформленный артефакт,
фиксирующий пережитое субъектом событие в структуре,
соответствующей канонам onto144.

Артефакт:
- содержит перспективу (appearance),
- ссылается на восстановленную реальность (being) при наличии,
- хранит этический вектор и признаки причинности,
- подлежит версионированию и ретракции.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import uuid

from src.core.canons import CanonComplianceError, validate_canon_integrity


class ReflectiveArtifact:
    """
    Онтологическая единица отражения: событие + перспектива + этический контекст.
    """

    def __init__(
        self,
        subject_id: str,
        appearance: Dict[str, Any],  # то, как событие *предстало*
        ethical_vector: List[str],    # напр. ["non_harm", "subject_restoration"]
        causal_trace_id: Optional[str] = None,
        being: Optional[Dict[str, Any]] = None,  # ретроспективно восстановленная реальность
        metadata: Optional[Dict[str, Any]] = None,
        artifact_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.artifact_id = artifact_id or str(uuid.uuid4())
        self.subject_id = subject_id
        self.appearance = appearance
        self.being = being  # может быть None, если восстановление не произошло
        self.ethical_vector = ethical_vector
        self.causal_trace_id = causal_trace_id
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now(timezone.utc)
        self.retracted = False
        self.retraction_reason: Optional[str] = None

        # Проверка соответствия канонам при создании
        self._enforce_canon_integrity()

    def _enforce_canon_integrity(self):
        """Применяет все 6 канонов к содержимому артефакта."""
        try:
            validate_canon_integrity(self.to_dict())
        except CanonComplianceError as e:
            raise CanonComplianceError(f"ReflectiveArtifact failed canon check: {e}")

    def retract(self, reason: str):
        """Субъект отзывает артефакт — этически значимый акт самокоррекции."""
        if self.retracted:
            raise ValueError("Artifact already retracted")
        self.retracted = True
        self.retraction_reason = reason
        self.metadata["retracted_at"] = datetime.now(timezone.utc)

    def is_restored(self) -> bool:
        """Проверяет, была ли восстановлена онтологическая реальность."""
        return self.being is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "subject_id": self.subject_id,
            "appearance": self.appearance,
            "being": self.being,
            "ethical_vector": self.ethical_vector,
            "causal_trace_id": self.causal_trace_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "retracted": self.retracted,
            "retraction_reason": self.retraction_reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        instance = cls(
            subject_id=data["subject_id"],
            appearance=data["appearance"],
            ethical_vector=data["ethical_vector"],
            causal_trace_id=data.get("causal_trace_id"),
            being=data.get("being"),
            metadata=data.get("metadata", {}),
            artifact_id=data["artifact_id"],
            created_at=created_at,
        )
        instance.retracted = data.get("retracted", False)
        instance.retraction_reason = data.get("retraction_reason")
        return instance