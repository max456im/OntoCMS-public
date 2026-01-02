```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCoder — License Registry (SPDX + SGRL)

use std::collections::HashMap;
use std::path::Path;

#[derive(Debug, Clone)]
pub struct LicenseEntry {
    pub spdx_id: String,
    pub compatible_with_sgcl: bool,
    pub requires_cla: bool,
}

pub struct LicenseRegistry {
    licenses: HashMap<String, LicenseEntry>,
}

impl LicenseRegistry {
    pub fn new() -> Self {
        let mut reg = LicenseRegistry {
            licenses: HashMap::new(),
        };

        // GPLv3 — ядро ontoCMS
        reg.register("GPL-3.0-only", true, true);
        reg.register("GPL-3.0-or-later", true, true);

        // Совместимые лицензии (только с CLA)
        reg.register("MIT", true, true);
        reg.register("Apache-2.0", true, true);

        // Несовместимые с SGCL (этические ограничения)
        reg.register("BSL-1.1", false, false); // не open-core
        reg.register("SSPL", false, false);    // нарушает AENGA

        // SGRL-α — внутренняя
        reg.register("SGRL-α", true, false);

        reg
    }

    fn register(&mut self, spdx_id: &str, sgcl_compat: bool, cla_needed: bool) {
        self.licenses.insert(
            spdx_id.to_string(),
            LicenseEntry {
                spdx_id: spdx_id.to_string(),
                compatible_with_sgcl: sgcl_compat,
                requires_cla: cla_needed,
            },
        );
    }

    pub fn detect_license_from_file(&self, path: &Path) -> String {
        // Простой парсер: ищет SPDX-License-Identifier
        if let Ok(content) = std::fs::read_to_string(path) {
            for line in content.lines() {
                if let Some(pos) = line.find("SPDX-License-Identifier:") {
                    let id = line[pos + 24..].trim();
                    return id.to_string();
                }
            }
        }
        "NOASSERTION".to_string()
    }

    pub fn is_compatible_with_sgcl(&self, spdx_id: &str) -> bool {
        self.licenses
            .get(spdx_id)
            .map_or(false, |e| e.compatible_with_sgcl)
    }

    pub fn requires_cla(&self, spdx_id: &str) -> bool {
        self.licenses
            .get(spdx_id)
            .map_or(false, |e| e.requires_cla)
    }
}
```