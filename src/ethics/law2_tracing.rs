```rust
// SPDX-License-Identifier: GPL-3.0-only
// Закон II Онтогенеза: Представление → Трассировка

use crate::core::activity_ledger::{OntoEvent, OntoPhase};

#[derive(Debug)]
pub enum TracingError {
    MissingCausalHash,
    FastPhaseWithoutContext,
    SocialProximityOutOfBounds,
}

/// Обязательная трассировка происхождения утверждения
pub fn enforce_tracing(event: &OntoEvent) -> Result<(), TracingError> {
    // Закон II: каждое представление должно иметь трассировку
    // В фазе Fast допускается отсутствие causal_hash, но требуется контекст
    if event.causal_hash.is_none() && event.phase != OntoPhase::Fast {
        return Err(TracingError::MissingCausalHash);
    }

    // В фазе Fast: должен быть указан социальный контекст
    if event.phase == OntoPhase::Fast && event.social_proximity == 0 {
        return Err(TracingError::FastPhaseWithoutContext);
    }

    // Социальная близость — от 1 до 100 (0 = отсутствие контекста → запрещено)
    if event.social_proximity > 100 {
        return Err(TracingError::SocialProximityOutOfBounds);
    }

    Ok(())
}
```