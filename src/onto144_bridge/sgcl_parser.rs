```rust
// SPDX-License-Identifier: GPL-3.0-only
// ontoCMS — SGCL Parser Bridge (Delegates to onto144)

use onto144::sgcl::{parse_sgcl_file, SgclValidationError};

/// Парсинг SGCL-файла из директории onto144/profiles/
pub fn parse_profile_sgcl(profile_id: &str) -> Result<onto144::Profile, SgclValidationError> {
    // onto144 предоставляет функцию загрузки по ID
    onto144::sgcl::load_profile_by_id(profile_id)
}

/// Валидация SGCL-синтаксиса (используется в CI)
pub fn validate_sgcl_syntax(content: &str) -> Result<(), SgclValidationError> {
    onto144::sgcl::validate_syntax(content)
}
```