```rust
// SPDX-License-Identifier: GPL-3.0-only
// ontoCMS — Bridge to onto144 (Profile Loader)

use onto144::{ProfileId as Onto144ProfileId, Profile, ProfileRegistry};

/// Адаптер: ProfileId из ontoCMS = ProfileId из onto144
pub type ProfileId = Onto144ProfileId;

/// Загрузка профиля из внешней библиотеки onto144
pub fn load_profile(id: &str) -> Option<Profile> {
    // onto144 гарантирует, что профиль существует и валиден
    onto144::registry::get_profile(id)
}

/// Проверка: профиль существует в onto-144
pub fn is_valid_profile(id: &str) -> bool {
    onto144::registry::is_valid_profile(id)
}

/// Получение всех 144 ID (для валидации в OntoCoder)
pub fn all_profile_ids() -> Vec<String> {
    onto144::registry::all_profile_ids()
}
```