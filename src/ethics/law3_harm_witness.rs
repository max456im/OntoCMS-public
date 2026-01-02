```rust
// SPDX-License-Identifier: GPL-3.0-only
// Закон III Онтогенеза: Разум → Свидетельство о вреде

use crate::core::activity_ledger::{OntoEvent, OntoPhase, ProfileId};
use crate::core::public_hub::PublicHub;
use crate::ethics::law1_attribution;
use crate::ethics::law2_tracing;

#[derive(Debug)]
pub enum HarmType {
    AENGAViolation,          // Внешнее управление
    BiometricExploitation,   // Извлечение биометрии без согласия
    EnergyValueInjection,    // Попытка внедрить энергетические метрики
    EthicsModuleBypass,      // Обход модулей этики
}

#[derive(Debug)]
pub struct HarmWitness {
    pub detected_harm: HarmType,
    pub violating_event_id: String,
    pub witness_profile: ProfileId,
    pub timestamp: u64,
    pub evidence: String,
}

/// Генерация свидетельства о вреде — даже если система не может его предотвратить
pub fn generate_harm_witness(
    harm: HarmType,
    violating_event: &OntoEvent,
    witness_profile: ProfileId,
) -> HarmWitness {
    HarmWitness {
        detected_harm: harm,
        violating_event_id: violating_event.id.clone(),
        witness_profile,
        timestamp: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64,
        evidence: format!(
            "Phase: {:?}, Payload keys: {:?}",
            violating_event.phase,
            violating_event.payload.as_object().map(|o| o.keys().collect::<Vec<_>>())
        ),
    }
}

/// Проверка события на признаки вреда
pub fn detect_harm(event: &OntoEvent) -> Option<HarmType> {
    let payload_str = event.payload.to_string().to_lowercase();

    // AENGA: попытка внешнего управления
    if payload_str.contains("remote_control") || payload_str.contains("override_ethics") {
        return Some(HarmType::AENGAViolation);
    }

    // Биометрическая эксплуатация
    if payload_str.contains("biometric") && !payload_str.contains("revocable_consent") {
        return Some(HarmType::BiometricExploitation);
    }

    // Энергетические метрики — запрещены
    if payload_str.contains("energy") || payload_str.contains("value_score") {
        return Some(HarmType::EnergyValueInjection);
    }

    // Обход этических модулей
    if payload_str.contains("skip_ethics") || payload_str.contains("bypass_law") {
        return Some(HarmType::EthicsModuleBypass);
    }

    None
}

/// Публикация свидетельства о вреде — даже в условиях отказа
pub async fn publish_harm_witness<H: PublicHub>(
    hub: &H,
    witness: &HarmWitness,
) -> Result<String, Box<dyn std::error::Error>> {
    // Свидетельство всегда создаётся в фазе Slow (рефлексия)
    let witness_event = OntoEvent {
        id: uuid::Uuid::new_v7(uuid::Timestamp::now(uuid::NoContext)).to_string(),
        profile_id: witness.witness_profile.clone(),
        phase: OntoPhase::Slow,
        payload: serde_json::json!({
            "harm_type": format!("{:?}", witness.detected_harm),
            "violating_event_id": witness.violating_event_id,
            "evidence": witness.evidence,
            "law3_witness": true
        }),
        social_proximity: 100, // максимальная ответственность
        causal_hash: None,
        timestamp: witness.timestamp,
    };

    // Принудительная валидация по Законам I и II
    law1_attribution::enforce_attribution(&witness_event)?;
    law2_tracing::enforce_tracing(&witness_event)?;

    // Публикация в Public Hub (IPFS/libp2p)
    let cid = hub.publish(&witness_event).await?;
    Ok(cid)
}
```