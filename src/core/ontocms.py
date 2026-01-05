# ontocms.py
# Core runtime coordinator for ontoCMS
# Licensed under GPLv3 + AENGA ethical covenant

from .canons import apply_all_canons
from .self_observer import SelfObserver

class OntoCMS:
    def __init__(self, config):
        self.config = config
        self.self_observer = SelfObserver()
        self.active_artifacts = []
        self.meta_ontology = None  # injected or loaded later

    def bootstrap(self):
        """Initializes system with ethical and structural integrity."""
        self.self_observer.start_monitoring()
        self.self_observer.assert_canonical_readiness()
        return self

    def process_artifact(self, artifact):
        """Processes a reflective artifact through canonical validation."""
        if not apply_all_canons(artifact, self.meta_ontology):
            raise ValueError("Artifact fails canonical integrity check")
        self.active_artifacts.append(artifact)
        return artifact

    def decompose_if_unrestorable(self, subject_id):
        """Triggers self-decomposition if subject restoration is impossible."""
        from protocols.subject_restoration_validator import can_restore_subject
        if not can_restore_subject(subject_id):
            from protocols.moral_judgment import trigger_self_revocation
            trigger_self_revocation(reason="irreversible subject fracture")