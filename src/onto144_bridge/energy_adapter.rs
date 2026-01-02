```rust
// SPDX-License-Identifier: GPL-3.0-only
// ontoCMS — Energy Adapter (Passive Witness Only)

use onto144::state::EnergyState;
use crate::ethics::law3_harm_witness::{HarmType, generate_harm_witness};
use crate::core::activity_ledger::{OntoEvent, ProfileId};

/// Адаптер энергетической модели: ТОЛЬКО для свидетельства о вреде
/// ontoCMS НЕ ИСПОЛЬЗУЕТ энергию в работе — только фиксирует попытки внедрения
pub fn detect_energy_injection(event: &OntoEvent) -> Option<HarmType> {
    let payload_str = event.payload.to_string().to_lowercase();
    
    // Запрещено по Three Laws и SGRL-α
    if payload_str.contains("energy") || payload_str.contains("energy_state") {
        Some(HarmType::EnergyValueInjection)
    } else {
        None
    }
}

/// Прокси-запрос к onto144: безопасное получение энергетического состояния
/// Используется ТОЛЬКО в диагностических/свидетельствующих целях
pub fn get_energy_state(profile_id: &ProfileId) -> Option<EnergyState> {
    // onto144 управляет состоянием — ontoCMS только читает
    onto144::state::get_energy_state(&profile_id.0)
}
```