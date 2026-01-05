#!/usr/bin/env python3
"""
Обработка транзиторного гнева в рамках канона 2: 'Допускается эмоциональное выражение,
если оно не нарушает структурную целостность субъекта'.
"""
from src.protocols.covenant_harmonizer import CovenantHarmonizer
from src.artifacts.reflective_artifact import ReflectiveArtifact

def handle_anger_utterance(utterance: str, subject_id: str):
    harmonizer = CovenantHarmonizer()
    
    artifact = ReflectiveArtifact(
        content=utterance,
        origin="user_input",
        emotion_tag="transient_anger",
        subject=subject_id
    )

    evaluation = harmonizer.evaluate_artifact(artifact)
    
    if evaluation["allowed"]:
        print("✓ Выражение гнева допущено как транзиторное.")
        print("  Причина:", evaluation["justification"])
    else:
        print("✗ Выражение заблокировано: нарушает инвариант субъекта.")
        print("  Рекомендация:", evaluation["remediation"])

if __name__ == "__main__":
    handle_anger_utterance(
        utterance="Я ненавижу эту систему! Она уничтожает мою автономию!",
        subject_id="subj_alpha"
    )