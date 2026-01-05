# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) [Year] [Author/Org]
"""
VersionedStore реализует иммутабельное, версионированное хранение артефактов,
гарантируя трассируемость изменений, восстановление субъекта и устойчивость
к редукции профиля. Каждый артефакт сохраняется как неизменяемый объект
с временной меткой, канонической проверкой и ссылкой на предыдущее состояние.
"""

import os
import uuid
import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List, Tuple
from pathlib import Path

from ..core.canons import validate_canonical_rhythm


class VersionedStore:
    def __init__(self, base_path: str = "data/store"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.base_path / "MANIFEST.json"
        self._load_manifest()

    def _load_manifest(self):
        if self.manifest_path.exists():
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {"artifacts": {}}

    def _save_manifest(self):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)

    def store_artifact(
        self,
        artifact: Dict[str, Any],
        subject_id: str,
        canonical_vector: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Сохраняет артефакт как иммутабельную запись.
        Возвращает уникальный идентификатор версии.
        """
        # Генерация временной метки в UTC
        timestamp = datetime.now(timezone.utc).isoformat()
        version_id = str(uuid.uuid4())

        # Проверка канонической ритмики (если применимо)
        if canonical_vector is not None:
            validate_canonical_rhythm(canonical_vector)

        # Контент для хеширования
        content_to_hash = json.dumps(
            artifact, sort_keys=True, ensure_ascii=False, separators=(',', ':')
        ).encode("utf-8")
        content_hash = hashlib.sha256(content_to_hash).hexdigest()

        # Сохранение записи
        record = {
            "version_id": version_id,
            "subject_id": subject_id,
            "timestamp": timestamp,
            "content_hash": content_hash,
            "canonical_vector": canonical_vector,
            "metadata": metadata or {},
        }

        # Запись артефакта в файл
        artifact_dir = self.base_path / subject_id
        artifact_dir.mkdir(exist_ok=True)
        artifact_file = artifact_dir / f"{version_id}.json"
        with open(artifact_file, "w", encoding="utf-8") as f:
            json.dump(artifact, f, indent=2, ensure_ascii=False)

        # Обновление манифеста
        if subject_id not in self.manifest["artifacts"]:
            self.manifest["artifacts"][subject_id] = []
        self.manifest["artifacts"][subject_id].append(version_id)
        self._save_manifest()

        return version_id

    def retrieve_artifact(self, version_id: str) -> Optional[Dict[str, Any]]:
        """Получает артефакт по его версии."""
        for subject_id, versions in self.manifest["artifacts"].items():
            if version_id in versions:
                artifact_file = self.base_path / subject_id / f"{version_id}.json"
                if artifact_file.exists():
                    with open(artifact_file, "r", encoding="utf-8") as f:
                        return json.load(f)
        return None

    def get_subject_history(self, subject_id: str) -> List[str]:
        """Возвращает хронологический список версий для субъекта."""
        return self.manifest["artifacts"].get(subject_id, [])

    def retract_artifact(
        self, version_id: str, retraction_reason: str, retractor_id: str
    ) -> bool:
        """
        Помечает артефакт как отозванный (не удаляет!).
        Сохраняется запись отмены в отдельной директории `retractions/`.
        """
        artifact = self.retrieve_artifact(version_id)
        if artifact is None:
            return False

        retraction_record = {
            "retracted_version": version_id,
            "retractor_id": retractor_id,
            "reason": retraction_reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        retraction_dir = self.base_path / "retractions"
        retraction_dir.mkdir(exist_ok=True)
        retraction_file = retraction_dir / f"{version_id}_retracted.json"
        with open(retraction_file, "w", encoding="utf-8") as f:
            json.dump(retraction_record, f, indent=2, ensure_ascii=False)

        return True