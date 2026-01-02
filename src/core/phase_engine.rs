```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCMS Core — Phase Engine (Ontogenetic State Manager)

use crate::core::activity_ledger::{OntoEvent, OntoPhase, ProfileId};

/// Движок управления фазами онтогенеза
pub struct PhaseEngine {
    current_phase: OntoPhase,
    profile: ProfileId,
}

impl PhaseEngine {
    pub fn new(initial_phase: OntoPhase, profile: ProfileId) -> Self {
        Self {
            current_phase: initial_phase,
            profile,
        }
    }

    pub fn current_phase(&self) -> &OntoPhase {
        &self.current_phase
    }

    /// Переход в новую фазу — с этической проверкой
    pub fn transition_to(&mut self, new_phase: OntoPhase) -> Result<(), PhaseError> {
        // Закон III: в фазе Slow разрешено свидетельствовать о вреде
        if self.current_phase == OntoPhase::Fast && new_phase == OntoPhase::Slow {
            // Разрешён: "slowing through reflection"
        } else if self.current_phase == OntoPhase::Heyday && new_phase == OntoPhase::Decline {
            // Деконструкция после синтеза — допустима
        } else if new_phase == OntoPhase::Fast && self.current_phase != OntoPhase::Decline {
            // Fast только из Decline (реакция на кризис)
            return Err(PhaseError::InvalidTransition);
        }

        self.current_phase = new_phase;
        Ok(())
    }

    /// Создание события в текущей фазе
    pub fn emit_event(&self, payload: serde_json::Value, social_proximity: u8) -> OntoEvent {
        let id = uuid::Uuid::new_v7(uuid::Timestamp::now(uuid::NoContext));
        OntoEvent {
            id: id.to_string(),
            profile_id: self.profile.clone(),
            phase: self.current_phase.clone(),
            payload,
            social_proximity,
            causal_hash: None, // Заполняется внешней системой
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_millis() as u64,
        }
    }
}

#[derive(Debug)]
pub enum PhaseError {
    InvalidTransition,
}
```