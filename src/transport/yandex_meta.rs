```rust
// SPDX-License-Identifier: GPL-3.0-only
// Yandex Metadata Hub — STRICTLY OPTIONAL

use crate::core::activity_ledger::OntoEvent;

#[derive(Debug)]
pub enum YandexMetaError {
    DisabledByDefault,
    AENGAViolation,
}

/// Интеграция с Yandex Metadata Hub
/// Доступна ТОЛЬКО если включена флагом компиляции `yandex-transport`
/// По умолчанию ОТКЛЮЧЕНА
#[cfg(feature = "yandex-transport")]
pub fn publish_to_yandex_meta(
    event: &OntoEvent,
    api_key: &str,
) -> Result<String, YandexMetaError> {
    // Проверка AENGA: запрет на передачу профильных данных
    if event.payload.to_string().contains("profile") || event.payload.to_string().contains("behavior") {
        return Err(YandexMetaError::AENGAViolation);
    }

    // Только анонимизированные данные
    let payload = serde_json::json!({
        "event_id": event.id,
        "phase": format!("{:?}", event.phase),
        "timestamp": event.timestamp
    });

    // В реальной реализации: HTTP-запрос к Yandex
    // Здесь — заглушка
    let _ = api_key; // чтобы не было предупреждения
    Ok("yandex-meta-id-123".to_string())
}

/// Если фича не включена — всегда ошибка
#[cfg(not(feature = "yandex-transport"))]
pub fn publish_to_yandex_meta(
    _event: &OntoEvent,
    _api_key: &str,
) -> Result<String, YandexMetaError> {
    Err(YandexMetaError::DisabledByDefault)
}
```