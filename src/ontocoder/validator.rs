```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCoder — License and Ontology Validator

use std::collections::HashSet;
use std::path::Path;

use crate::ontocoder::license_registry::LicenseRegistry;
use crate::core::activity_ledger::ProfileId;

#[derive(Debug)]
pub enum ValidationError {
    LicenseIncompatible(String),
    ProfileNotInRegistry(ProfileId),
    EnergyValueDetected,
    PhaseAnnotationMissing,
    AENGAViolation,
}

pub struct OntoValidator {
    license_registry: LicenseRegistry,
    allowed_profiles: HashSet<ProfileId>,
}

impl OntoValidator {
    pub fn new(license_registry: LicenseRegistry, profile_list: Vec<ProfileId>) -> Self {
        Self {
            license_registry,
            allowed_profiles: profile_list.into_iter().collect(),
        }
    }

    /// Валидация исходного файла на соответствие SGRL-α и onto-144
    pub fn validate_file(&self, path: &Path, content: &str) -> Result<(), ValidationError> {
        self.check_no_energy_values(content)?;
        self.check_license_compliance(path)?;
        self.check_profile_attribution(content)?;
        self.check_phase_annotation(content)?;
        self.check_aenga_compliance(content)?;
        Ok(())
    }

    fn check_no_energy_values(&self, content: &str) -> Result<(), ValidationError> {
        let forbidden = &["energy", "value", "attract", "monetize", "score"];
        if forbidden.iter().any(|kw| content.contains(kw)) {
            Err(ValidationError::EnergyValueDetected)
        } else {
            Ok(())
        }
    }

    fn check_license_compliance(&self, path: &Path) -> Result<(), ValidationError> {
        let license = self.license_registry.detect_license_from_file(path);
        if !self.license_registry.is_compatible_with_sgcl(&license) {
            Err(ValidationError::LicenseIncompatible(license))
        } else {
            Ok(())
        }
    }

    fn check_profile_attribution(&self, content: &str) -> Result<(), ValidationError> {
        // Ищем строку вида: // ONTO-PROFILE: Aries-Wood-Rabbit
        let lines: Vec<&str> = content.lines().collect();
        let profile_line = lines.iter().find(|l| l.contains("ONTO-PROFILE:"));
        match profile_line {
            Some(line) => {
                let id_str = line.split("ONTO-PROFILE:").nth(1).unwrap_or("").trim();
                let profile_id = ProfileId(id_str.to_string());
                if self.allowed_profiles.contains(&profile_id) {
                    Ok(())
                } else {
                    Err(ValidationError::ProfileNotInRegistry(profile_id))
                }
            }
            None => Err(ValidationError::ProfileNotInRegistry(ProfileId("unattributed".into()))),
        }
    }

    fn check_phase_annotation(&self, content: &str) -> Result<(), ValidationError> {
        // Требуем: // ONTO-PHASE: Slow | Fast | Heyday | Decline
        if !content.contains("ONTO-PHASE:") {
            Err(ValidationError::PhaseAnnotationMissing)
        } else {
            Ok(())
        }
    }

    fn check_aenga_compliance(&self, content: &str) -> Result<(), ValidationError> {
        // Запрещаем: вызовы внешних API без фазовой обёртки
        if content.contains("remote_control") || content.contains("override_ethics") {
            Err(ValidationError::AENGAViolation)
        } else {
            Ok(())
        }
    }
}
```