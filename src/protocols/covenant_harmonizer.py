# covenant_harmonizer.py
# Часть ontoCMS — этическая гармонизация через иерархию ковенантов
# Лицензия: GPL-3.0-or-later + AENGA Covenant

from typing import Dict, List, Optional, Any
from .covenant_recognition import CovenantRecognitionProtocol
from .covenant_accountability import CovenantAccountabilityProtocol
from .covenant_affirmation import CovenantAffirmationProtocol

class CovenantHarmonizer:
    """
    Координирует три ковенанта:
      - Культура (Recognition): что признаётся допустимым
      - Деятельность (Accountability): что несёт ответственность
      - Свобода (Affirmation): что утверждает автономию субъекта

    Гармонизация означает:
      - Разрешение конфликтов между ковенантами
      - Приоритизация восстановления субъекта при нарушении
      - Отказ от действия, если гармония невозможна
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.recognition = CovenantRecognitionProtocol(config)
        self.accountability = CovenantAccountabilityProtocol(config)
        self.affirmation = CovenantAffirmationProtocol(config)

    def harmonize(self, activity: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Возвращает гармонизированный акт или отказ с причиной.
        Формат результата:
        {
            "allowed": bool,
            "reason": Optional[str],
            "harmony_score": float (0.0–1.0),
            "covenant_alignment": {
                "recognition": bool,
                "accountability": bool,
                "affirmation": bool
            }
        }
        """
        rec = self.recognition.evaluate(activity, context)
        acc = self.accountability.evaluate(activity, context)
        aff = self.affirmation.evaluate(activity, context)

        alignment = {
            "recognition": rec["valid"],
            "accountability": acc["valid"],
            "affirmation": aff["valid"]
        }

        # Приоритет: утверждение субъектности (Affirmation)
        if not aff["valid"]:
            return {
                "allowed": False,
                "reason": "Affirmation covenant violated: activity undermines subject autonomy",
                "harmony_score": 0.0,
                "covenant_alignment": alignment
            }

        # Вторичный приоритет: ответственность за вред
        if not acc["valid"]:
            return {
                "allowed": False,
                "reason": "Accountability covenant violated: unmitigated harm or incitement",
                "harmony_score": 0.0,
                "covenant_alignment": alignment
            }

        # Третичный: признание в культурном/онтологическом контексте
        if not rec["valid"]:
            # Но: если и Affirmation, и Accountability — OK, возможно временное исключение
            if self._is_temporary_transgression_allowed(activity, context):
                return {
                    "allowed": True,
                    "reason": "Temporary cultural transgression permitted under affirmation & accountability",
                    "harmony_score": 0.6,
                    "covenant_alignment": alignment
                }
            else:
                return {
                    "allowed": False,
                    "reason": "Recognition covenant violated: activity lacks ontological grounding",
                    "harmony_score": 0.3,
                    "covenant_alignment": alignment
                }

        # Все ковенанты соблюдены
        return {
            "allowed": True,
            "reason": "Full covenant alignment achieved",
            "harmony_score": 1.0,
            "covenant_alignment": alignment
        }

    def _is_temporary_transgression_allowed(self, activity: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Проверяет, может ли транзитное нарушение признания быть допущено
        (например, выражение гнева в безопасной форме — см. тесты).
        """
        # Пример: transient_anger — разрешено, если не причиняет вреда
        if activity.get("type") == "emotive_utterance" and activity.get("emotion") == "anger":
            if context.get("safety_context") == "contained_reflection":
                return True
        return False