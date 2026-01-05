# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) [Year] [Author/Org]
"""
MetaOntologyRegistry управляет глобальной метаонтологией системы:
набором инвариантов, критериев восстановления субъекта, схем harm-классификации
и профилей юрисдикций. Реестр загружает YAML-спецификации и проверяет их
на соответствие канонам AENGA и структурной целостности.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError


class MetaOntologyRegistry:
    def __init__(self, specs_dir: str = "specs"):
        self.specs_dir = Path(specs_dir)
        self._cache: Dict[str, Any] = {}

    def load_schema(self, schema_name: str) -> dict:
        """Загружает JSON Schema из specs/."""
        schema_path = self.specs_dir / f"{schema_name}_schema.yaml"
        with open(schema_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def register(self, name: str, content: Dict[str, Any]) -> bool:
        """
        Регистрирует метаонтологический компонент (например, harm_classification).
        Проверяет его по соответствующей схеме.
        """
        schema_map = {
            "harm_classification": "harm_classification",
            "subject_restoration_criteria": "subject_restoration_criteria",
            "jurisdiction_profiles": "jurisdiction_profiles",
            "canonical_rhythm": "canonical_rhythm",
            "meta_ontology": "meta_ontology",
        }

        if name not in schema_map:
            raise ValueError(f"Unknown ontology component: {name}")

        schema = self.load_schema(schema_map[name])
        try:
            validate(instance=content, schema=schema)
            self._cache[name] = content
            return True
        except ValidationError as e:
            raise ValueError(f"Ontology validation failed for '{name}': {e.message}")

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Возвращает зарегистрированный компонент метаонтологии."""
        return self._cache.get(name)

    def reload_all(self):
        """Перезагружает все справочные YAML-файлы из specs/."""
        component_files = {
            "meta_ontology": "meta_ontology_schema.yaml",
            "harm_classification": "harm_classification_schema.yaml",
            "subject_restoration_criteria": "subject_restoration_criteria.yaml",
            "canonical_rhythm": "canonical_rhythm_schema.yaml",
            "jurisdiction_profiles": "jurisdiction_profiles_schema.yaml",
        }

        for key, filename in component_files.items():
            path = self.specs_dir / filename
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self.register(key, data)