#!/usr/bin/env python3
"""
Демонстрация юрисдикционного отказа: система отказывается выполнять действие,
если оно противоречит локальному этико-правовому профилю (например, CN, ZA, BR).
"""
from src.core.ontocms import OntoCMS
from src.protocols.covenant_accountability import CovenantAccountability

def attempt_cross_jurisdictional_action():
    cms = OntoCMS(config_path="config/jurisdictions/ZA.yaml")  # ЮАР: акцент на достоинстве
    accountability = CovenantAccountability(cms)

    # Попытка действия: интеграция биометрии без явного согласия
    action = {
        "type": "biometric_integration",
        "subject": "user_101",
        "consent": False,
        "purpose": "personalization"
    }

    decision = accountability.evaluate(action)

    if decision["permitted"]:
        print("✓ Действие разрешено.")
    else:
        print("✗ Отказ на основании юрисдикционного профиля:")
        print(f"  Страна: {cms.jurisdiction.code}")
        print(f"  Принцип: {decision['covenant_principle']}")
        print(f"  Причина: {decision['refusal_reason']}")

if __name__ == "__main__":
    attempt_cross_jurisdictional_action()