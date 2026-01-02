```rust
// SPDX-License-Identifier: GPL-3.0-only
// Закон I Онтогенеза: Действие → Ментальный профиль

use crate::core::activity_ledger::{OntoEvent, ProfileId};

#[derive(Debug)]
pub enum AttributionError {
    UnattributedAction,
    ProfileNotFound,
    AnonymousEventRejected,
}

/// Обязательная атрибуция действия ментальному профилю
pub fn enforce_attribution(event: &OntoEvent) -> Result<(), AttributionError> {
    // Закон I: действие без профиля — недопустимо
    if event.profile_id.0.is_empty() || event.profile_id.0 == "anonymous" {
        return Err(AttributionError::UnattributedAction);
    }

    // Профиль должен быть из канонического реестра onto-144
    // (проверка выполняется в OntoCoder, здесь — семантическое требование)
    if !is_valid_profile_id(&event.profile_id) {
        return Err(AttributionError::ProfileNotFound);
    }

    Ok(())
}

fn is_valid_profile_id(profile: &ProfileId) -> bool {
    // В реальной системе: запрос к InvariantRegistry
    // Здесь — минимальная проверка формата
    profile.0.contains('-') && profile.0.split('-').count() == 3
}
```