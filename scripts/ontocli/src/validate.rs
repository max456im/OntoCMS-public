```rust
use clap::Args;
use std::path::PathBuf;

use ontocms_ontocoder::validator::OntoValidator;
use ontocms_ontocoder::license_registry::LicenseRegistry;
use ontocms_forms::invariant_registry::InvariantRegistry;

#[derive(Args)]
pub struct Args {
    /// Путь к файлу или директории
    #[arg(value_name = "PATH")]
    pub path: PathBuf,
}

pub fn run(args: &Args) -> Result<(), Box<dyn std::error::Error>> {
    // Загрузка профилей
    let mut registry = InvariantRegistry::new();
    registry.load_from_disk("../../src/forms/profiles")?;
    let profiles = registry.all_ids().into_iter().map(|id| ontocms_core::activity_ledger::ProfileId(id)).collect();

    // Валидатор
    let license_reg = LicenseRegistry::new();
    let validator = OntoValidator::new(license_reg, profiles);

    if args.path.is_file() {
        validate_file(&validator, &args.path)?;
    } else if args.path.is_dir() {
        for entry in std::fs::read_dir(&args.path)? {
            let entry = entry?;
            if entry.path().extension() == Some(std::ffi::OsStr::new("rs")) {
                validate_file(&validator, &entry.path())?;
            }
        }
    }

    println!("✅ Validation passed: compliant with SGRL-α and Three Laws");
    Ok(())
}

fn validate_file(validator: &OntoValidator, path: &std::path::Path) -> Result<(), Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(path)?;
    validator.validate_file(path, &content)?;
    println!("   ✔ {}", path.display());
    Ok(())
}
```