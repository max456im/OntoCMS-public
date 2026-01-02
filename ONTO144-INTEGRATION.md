```markdown
# Интеграция ontoCMS с onto144

## Принцип

**onto144** — единственный источник истины для:
- 144 ментальных профилей,
- Онтологических инвариант,
- Энергетической модели,
- SGCL-синтаксиса.

**ontoCMS** не содержит, не генерирует и не изменяет профили. Он **использует** onto144 как библиотеку.

## Установка

Убедитесь, что репозиторий `onto144` доступен:

```bash
/workspace
├── ontoCMS/      # этот проект
└── onto144/      # https://github.com/ontocms/onto144
```

Или укажите Git-зависимость в `Cargo.toml`.

## Использование в коде

### Загрузка профиля
```rust
use ontocms::onto144_bridge::profile_loader;

let profile = profile_loader::load_profile("Aries-Fire-Choleric")
    .expect("Profile must exist in onto144");
```

### Валидация в OntoCoder
```rust
use ontocms::onto144_bridge::profile_loader;

if !profile_loader::is_valid_profile("Invalid-Profile") {
    // Отклонить
}
```

### Обнаружение энергетического вреда
```rust
use ontocms::onto144_bridge::energy_adapter;

if let Some(harm) = energy_adapter::detect_energy_injection(&event) {
    let witness = generate_harm_witness(harm, &event, profile_id);
    // Опубликовать свидетельство
}
```

## Важно

- **Никогда не копируйте профили в ontoCMS**.
- **Не модифицируйте onto144 напрямую** — вносите изменения в его репозиторий.
- **Энергетическая модель не используется в логике ontoCMS** — только для Law III.
```
