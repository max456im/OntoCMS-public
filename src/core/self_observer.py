# self_observer.py
# Implements introspective monitoring aligned with SGCL & AENGA

from protocols.canonical_tester import CanonicalTester

class SelfObserver:
    def __init__(self):
        self.status = "idle"
        self.canon_violations = []

    def start_monitoring(self):
        self.status = "active"

    def assert_canonical_readiness(self):
        tester = CanonicalTester()
        results = tester.run_all_canons()
        if not all(results.values()):
            self.status = "compromised"
            self.canon_violations = [k for k, v in results.items() if not v]
            raise RuntimeError(f"Canonical readiness failed: {self.canon_violations}")

    def log_intentional_state(self, state):
        """Records internal state for reflective recurrence and audit."""
        # This supports the SUBJECT-RESTORATION-PRINCIPLE
        pass  # actual storage delegated to storage/versioned_store.py