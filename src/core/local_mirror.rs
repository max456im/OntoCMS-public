```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCMS Core — Local Mirror (No External Dependency)

use std::collections::HashMap;
use std::fs;
use std::path::Path;

use crate::core::activity_ledger::{OntoEvent, ProfileId};

/// Локальное зеркало событий — автономное, не требует сети
pub struct LocalMirror {
    base_path: String,
    loaded_profiles: HashMap<ProfileId, bool>,
}

impl LocalMirror {
    pub fn new(base_dir: &str) -> Self {
        let path = format!("{}/local_mirror", base_dir);
        fs::create_dir_all(&path).expect("Failed to create local_mirror dir");
        Self {
            base_path: path,
            loaded_profiles: HashMap::new(),
        }
    }

    /// Сохранение события на диск — идемпотентно
    pub fn persist(&self, event: &OntoEvent) {
        let file_path = format!(
            "{}/{}/{}.json",
            self.base_path,
            event.profile_id.0,
            event.id
        );
        fs::create_dir_all(Path::new(&file_path).parent().unwrap()).ok();
        let _ = fs::write(&file_path, serde_json::to_vec_pretty(event).unwrap());
    }

    /// Загрузка всех событий профиля
    pub fn load_profile(&mut self, profile: &ProfileId) -> Vec<OntoEvent> {
        if self.loaded_profiles.get(profile).copied() == Some(true) {
            return vec![]; // Уже загружено — избегаем дублирования
        }

        let profile_dir = format!("{}/{}", self.base_path, profile.0);
        let mut events = vec![];

        if let Ok(entries) = fs::read_dir(&profile_dir) {
            for entry in entries.flatten() {
                if let Ok(content) = fs::read_to_string(entry.path()) {
                    if let Ok(event) = serde_json::from_str::<OntoEvent>(&content) {
                        events.push(event);
                    }
                }
            }
        }

        self.loaded_profiles.insert(profile.clone(), true);
        events
    }

    /// Проверка: есть ли локально событие
    pub fn has_event(&self, profile: &ProfileId, event_id: &str) -> bool {
        let path = format!("{}/{}/{}.json", self.base_path, profile.0, event_id);
        Path::new(&path).exists()
    }
}
```