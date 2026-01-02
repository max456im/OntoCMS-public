```rust
// SPDX-License-Identifier: GPL-3.0-only
// Darwin Core Export — Only Public, Non-Biometric Events

use crate::core::activity_ledger::OntoEvent;
use serde::Serialize;

#[derive(Serialize)]
pub struct DarwinCoreRecord {
    pub occurrence_id: String,       // ontoCMS event ID
    pub event_date: String,          // ISO 8601
    pub scientific_name: Option<String>,
    pub locality: Option<String>,
    pub country: Option<String>,
    pub recorded_by: String,         // onto-144 profile ID
    pub basis_of_record: String,     // "MachineObservation"
    pub ontocms_phase: String,       // Fast/Slow/Heyday/Decline
}

/// Преобразование онтологического события в Darwin Core
/// Только если событие НЕ содержит биометрию и НЕ приватное
pub fn export_to_darwin_core(event: &OntoEvent) -> Result<DarwinCoreRecord, DarwinCoreError> {
    // Запрет на биометрию (Law III)
    if event.payload.to_string().to_lowercase().contains("biometric") {
        return Err(DarwinCoreError::BiometricDataDetected);
    }

    // Только публичные события (например, связанные с наблюдением природы)
    if !is_public_biodiversity_event(event) {
        return Err(DarwinCoreError::NonPublicEvent);
    }

    let timestamp = chrono::NaiveDateTime::from_timestamp_opt(
        (event.timestamp / 1000) as i64,
        0,
    )
    .ok_or(DarwinCoreError::InvalidTimestamp)?
    .format("%Y-%m-%dT%H:%M:%SZ")
    .to_string();

    Ok(DarwinCoreRecord {
        occurrence_id: event.id.clone(),
        event_date: timestamp,
        scientific_name: extract_scientific_name(event),
        locality: extract_locality(event),
        country: extract_country(event),
        recorded_by: event.profile_id.0.clone(),
        basis_of_record: "MachineObservation".to_string(),
        ontocms_phase: format!("{:?}", event.phase),
    })
}

fn is_public_biodiversity_event(event: &OntoEvent) -> bool {
    if let Some(obj) = event.payload.as_object() {
        obj.contains_key("scientific_name") || obj.contains_key("species_observation")
    } else {
        false
    }
}

fn extract_scientific_name(event: &OntoEvent) -> Option<String> {
    event
        .payload
        .get("scientific_name")
        .and_then(|v| v.as_str())
        .map(|s| s.to_string())
}

fn extract_locality(event: &OntoEvent) -> Option<String> {
    event
        .payload
        .get("locality")
        .and_then(|v| v.as_str())
        .map(|s| s.to_string())
}

fn extract_country(event: &OntoEvent) -> Option<String> {
    event
        .payload
        .get("country")
        .and_then(|v| v.as_str())
        .map(|s| s.to_string())
}

#[derive(Debug)]
pub enum DarwinCoreError {
    BiometricDataDetected,
    NonPublicEvent,
    InvalidTimestamp,
}
```