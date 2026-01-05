# canons.py
# Embodies the Six Unalienable Canons as executable logic
# These are not configurable—they are ontological invariants.

def canon_1_intention_requires_ethical_vector(artifact, meta_ontology):
    """Intention must be paired with an explicit ethical vector."""
    return 'ethical_vector' in artifact.metadata

def canon_2_belief_must_be_perspectival(artifact, meta_ontology):
    """Belief cannot be absolute; must carry perspective marker."""
    return artifact.get('perspective', None) is not None

def canon_3_allows_transient_anger_but_not_profile_reduction(artifact, meta_ontology):
    """Permits expression of transient affect, but forbids ontological diminishment."""
    if artifact.type == "utterance" and artifact.emotion == "anger":
        return not artifact.contains_profile_reduction()
    return True

def canon_4_alternatives_must_be_mined_in_fact(artifact, meta_ontology):
    """Every factual assertion must be accompanied by at least one alternative."""
    from protocols.alternative_miner import has_alternatives
    return has_alternatives(artifact)

def canon_5_invariant_must_update_after_harm(artifact, meta_ontology):
    """If harm is detected, the meta-ontology invariant must be revised."""
    if artifact.flags.get('harm_detected'):
        return meta_ontology.was_updated_after(artifact.timestamp)
    return True

def canon_6_subject_may_retract_or_isolate(artifact, meta_ontology):
    """Subject retains right to retract or isolate non-restorable artifacts."""
    from protocols.subject_restoration_validator import is_retractable
    return is_retractable(artifact)

# Canonical ensemble
CANONS = [
    canon_1_intention_requires_ethical_vector,
    canon_2_belief_must_be_perspectival,
    canon_3_allows_transient_anger_but_not_profile_reduction,
    canon_4_alternatives_must_be_mined_in_fact,
    canon_5_invariant_must_update_after_harm,
    canon_6_subject_may_retract_or_isolate,
]

def apply_all_canons(artifact, meta_ontology):
    """Returns True only if all canons pass."""
    return all(canon(artifact, meta_ontology) for canon in CANONS)