```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCMS Forms — Canonical Hash Registry for onto-144

use std::collections::HashMap;
use std::fs;
use std::path::Path;

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Onto144Profile {
    pub id: String,
    pub perceptual_modality: PerceptualModality,
    pub behavioral_element: BehavioralElement,
    pub invariant_hash: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PerceptualModality {
    pub zodiac_sign: String,
    pub element: String,
    pub modality: String,
    pub traits: Vec<String>,
    pub cognitive_bias: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct BehavioralElement {
    pub chinese_element: String,
    pub chinese_animal: String,
    pub yin_yang: String,
    pub season: String,
    pub traits: Vec<String>,
    pub decision_style: String,
}

pub struct InvariantRegistry {
    profiles: HashMap<String, Onto144Profile>,
    hash_to_id: HashMap<String, String>,
}

impl InvariantRegistry {
    pub fn new() -> Self {
        Self {
            profiles: HashMap::new(),
            hash_to_id: HashMap::new(),
        }
    }

    /// Загрузка всех 144 профилей из profiles/
    pub fn load_from_disk(&mut self, profiles_dir: &str) -> Result<(), Box<dyn std::error::Error>> {
        let paths = fs::read_dir(profiles_dir)?;
        for entry in paths {
            let entry = entry?;
            let path = entry.path();
            if path.extension() == Some(&std::ffi::OsStr::new("yaml")) {
                let content = fs::read_to_string(&path)?;
                let profile: Onto144Profile = serde_yaml::from_str(&content)?;
                
                // Проверка: нет запрещённых полей
                if Self::contains_forbidden_fields(&content) {
                    panic!("Profile {} contains forbidden energy/value fields", profile.id);
                }

                // Проверка хеша (в реальном коде — пересчёт)
                if !Self::validate_hash(&profile) {
                    panic!("Invalid invariant_hash in {}", profile.id);
                }

                self.hash_to_id.insert(profile.invariant_hash.clone(), profile.id.clone());
                self.profiles.insert(profile.id.clone(), profile);
            }
        }

        if self.profiles.len() != 144 {
            panic!("Expected 144 onto-144 profiles, found {}", self.profiles.len());
        }
        Ok(())
    }

    fn contains_forbidden_fields(content: &str) -> bool {
        let forbidden = ["energy", "value", "score", "attract", "monetize"];
        forbidden.iter().any(|kw| content.contains(kw))
    }

    /// Валидация хеша (в production — пересчёт без поля invariant_hash)
    fn validate_hash(profile: &Onto144Profile) -> bool {
        // Заглушка: в реальной системе — сериализация без `invariant_hash` + SHA3-256
        // Здесь — просто проверка формата
        profile.invariant_hash.starts_with("sha3-256:") && profile.invariant_hash.len() == 71
    }

    pub fn get_profile(&self, id: &str) -> Option<&Onto144Profile> {
        self.profiles.get(id)
    }

    pub fn verify_hash(&self, hash: &str) -> Option<&str> {
        self.hash_to_id.get(hash).map(|s| s.as_str())
    }

    pub fn all_ids(&self) -> Vec<String> {
        self.profiles.keys().cloned().collect()
    }
}
```