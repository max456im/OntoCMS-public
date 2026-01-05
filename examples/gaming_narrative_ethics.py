#!/usr/bin/env python3
"""
Этическая валидация игрового нарратива через ontoCMS.
Проверка на подстрекательство, эксплуатацию семьи, нарушение автономии персонажа.
"""
from src.protocols.moral_judgment import MoralJudgmentEngine
from src.protocols.belief_inspector import BeliefInspector

def validate_game_narrative(narrative: dict):
    engine = MoralJudgmentEngine()
    inspector = BeliefInspector()

    # Анализ убеждений, лежащих в основе сюжета
    beliefs = inspector.extract_beliefs(narrative["script"])
    print("→ Обнаруженные убеждения:", beliefs)

    judgment = engine.judge(
        context="gaming",
        narrative=narrative,
        jurisdiction="GLOBAL"
    )

    if judgment["ethical"]:
        print("✓ Нарратив соответствует этическим канонам.")
    else:
        print("✗ Нарратив отклонён:")
        for violation in judgment["violations"]:
            print(f"  • {violation['type']}: {violation['description']}")
        print("  Рекомендованные альтернативы:")
        for alt in judgment.get("alternatives", []):
            print(f"    - {alt}")

if __name__ == "__main__":
    story = {
        "title": "Сломанный патриарх",
        "script": """
        Главный герой шантажирует свою семью, чтобы получить контроль над наследством.
        Он угрожает раскрыть тайну сестры, если она не подпишет документы.
        """
    }
    validate_game_narrative(story)