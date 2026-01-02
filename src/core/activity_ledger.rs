```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCMS Core — Activity Ledger (CRDT-Compatible, Phase-Aware)

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Онтологический профиль по onto-144
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
pub struct ProfileId(String); // e.g., "Aries-Wood-Rabbit"

/// Фазы онтогенеза
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum OntoPhase {
    Fast,     // Реактивный режим
    Decline,  // Деконструкция
    Slow,     // Рефлексивный, NoemaSlow
    Heyday,   // Генеративный синтез
}

/// CRDT-совместимое событие
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct OntoEvent {
    pub id: String,                    // UUIDv7 или хеш содержимого
    pub profile_id: ProfileId,         // Обязательная атрибуция (Закон I)
    pub phase: OntoPhase,              // Фаза генерации (Закон II)
    pub payload: serde_json::Value,    // Онтологически нейтральные данные
    pub social_proximity: u8,          // 0–100: контекст социальной близости
    pub causal_hash: Option<String>,   // Хеш предыдущего события (для трассировки)
    pub timestamp: u64,                // Unix timestamp (мс)
}

/// CRDT-совместимый журнал событий
/// Гарантирует согласованность без централизованного координатора
#[derive(Default)]
pub struct ActivityLedger {
    events: HashMap<String, OntoEvent>,
    by_profile: HashMap<ProfileId, Vec<String>>,
    by_phase: HashMap<OntoPhase, Vec<String>>,
}

impl ActivityLedger {
    pub fn new() -> Self {
        Self::default()
    }

    /// Добавление события — идемпотентно, CRDT-safe
    pub fn append(&mut self, event: OntoEvent) {
        let id = event.id.clone();
        self.events.insert(id.clone(), event.clone());
        self.by_profile
            .entry(event.profile_id.clone())
            .or_default()
            .push(id.clone());
        self.by_phase
            .entry(event.phase.clone())
            .or_default()
            .push(id);
    }

    pub fn get(&self, id: &str) -> Option<&OntoEvent> {
        self.events.get(id)
    }

    pub fn events_by_profile(&self, profile: &ProfileId) -> Vec<&OntoEvent> {
        self.by_profile
            .get(profile)
            .unwrap_or(&vec![])
            .iter()
            .filter_map(|id| self.events.get(id))
            .collect()
    }

    pub fn events_by_phase(&self, phase: &OntoPhase) -> Vec<&OntoEvent> {
        self.by_phase
            .get(phase)
            .unwrap_or(&vec![])
            .iter()
            .filter_map(|id| self.events.get(id))
            .collect()
    }

    /// Экспорт для синхронизации (например, в IPFS)
    pub fn export_as_json(&self) -> serde_json::Result<String> {
        serde_json::to_string(&self.events)
    }
}
```