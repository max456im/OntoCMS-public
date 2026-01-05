#!/usr/bin/env python3
"""
Демонстрация канонического цикла ontoCMS: от намерения к инварианту.
Использует core.canons и protocols.canonical_tester для валидации этического вектора.
"""
from src.core.ontocms import OntoCMS
from src.protocols.canonical_tester import run_canonical_cycle

def main():
    cms = OntoCMS(config_path="config/default.yaml")
    
    # Пример этического намерения: "обновить профиль пользователя"
    intention = {
        "verb": "update_profile",
        "subject": "user_789",
        "context": {"platform": "gaming", "region": "ZA"},
        "ethical_vector": ["consent", "non_reduction", "subject_dignity"]
    }

    print("→ Запуск канонического цикла...")
    result = run_canonical_cycle(cms, intention)

    if result["passed"]:
        print("✓ Цикл пройден. Инвариант обновлён.")
        print(f"  Новый инвариант: {result['invariant_hash']}")
    else:
        print("✗ Цикл провален. Причина:", result["failure_reason"])
        for artifact in result.get("reflective_artifacts", []):
            print(f"  Артефакт: {artifact.summary()}")

if __name__ == "__main__":
    main()