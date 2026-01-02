```rust
use clap::Args;
use std::path::PathBuf;

#[derive(Args)]
pub struct Args {
    /// Путь к репозиторию
    #[arg(value_name = "REPO_PATH", default_value = ".")]
    pub repo_path: PathBuf,

    /// Строгий режим: завершать с ошибкой при любом нарушении
    #[arg(long)]
    pub strict: bool,
}

pub fn run(args: &Args) -> Result<(), Box<dyn std::error::Error>> {
    let forbidden = ["energy", "value_score", "attractiveness", "monetize", "biometric_raw"];
    let mut violations = 0;

    for entry in walkdir::WalkDir::new(&args.repo_path) {
        let entry = entry?;
        if entry.file_type().is_file() {
            let path = entry.path();
            if let Ok(content) = std::fs::read_to_string(path) {
                for word in &forbidden {
                    if content.contains(word) {
                        eprintln!("🔍 VIOLATION in {}: forbidden term '{}'", path.display(), word);
                        violations += 1;
                    }
                }
            }
        }
    }

    if violations > 0 {
        eprintln!("\n⚠️  Found {} ontological violations.", violations);
        if args.strict {
            std::process::exit(1);
        }
    } else {
        println!("✅ No energy-value or biometric violations detected.");
    }

    Ok(())
}
```