```rust
use clap::Args;
use std::fs;

#[derive(Args)]
pub struct Args {
    /// ONTO-PROFILE: e.g., Aries-Wood-Rabbit
    #[arg(long)]
    pub profile: String,

    /// ONTO-PHASE: Fast | Slow | Heyday | Decline
    #[arg(long)]
    pub phase: String,

    /// Сообщение коммита
    #[arg(long)]
    pub message: String,

    /// Путь к файлам (опционально)
    #[arg(long, default_value = ".")]
    pub path: String,
}

pub async fn run(args: &Args) -> Result<(), Box<dyn std::error::Error>> {
    // 1. Проверка профиля
    if !args.profile.contains('-') || args.profile.split('-').count() != 3 {
        eprintln!("❌ Invalid ONTO-PROFILE format. Use: Zodiac-Element-Animal");
        std::process::exit(1);
    }

    // 2. Проверка фазы
    if !["Fast", "Slow", "Heyday", "Decline"].contains(&args.phase.as_str()) {
        eprintln!("❌ Invalid ONTO-PHASE. Use: Fast | Slow | Heyday | Decline");
        std::process::exit(1);
    }

    // 3. Генерация метаданных коммита
    let metadata = format!(
        "// ONTO-PROFILE: {}\n// ONTO-PHASE: {}\n// SPDX-License-Identifier: GPL-3.0-only\n",
        args.profile, args.phase
    );

    // 4. Добавление метаданных в каждый файл (упрощённо)
    // В реальности — через git hooks или patch
    println!("📝 Preparing ontological commit:");
    println!("   Profile: {}", args.profile);
    println!("   Phase: {}", args.phase);
    println!("   Message: {}", args.message);
    println!("\n⚠️  Run `git commit -m \"{}\"` manually after adding files.", args.message);
    println!("   Ensure all files contain the above metadata.");

    Ok(())
}
```