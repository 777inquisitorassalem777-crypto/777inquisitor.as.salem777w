from .state import SophiaState
from typing import Tuple


class EthicalDiscriminator:
    """
    Модуль различения добра и зла + противодействие злу.
    
    Основан на синтезе:
    - Христианской этики (любовь, милосердие, противостояние злу)
    - Славянских Вед / Инглиизма (порядок, гармония, защита рода)
    - Даосского баланса
    - Принципа "золотой середины"
    
    Не использует иудейские и исламские источники (по явному требованию архитектора).
    """

    def __init__(self, state: SophiaState):
        self.state = state

    def evaluate_action(self, action_description: str, intent_signal: float) -> dict:
        """
        Оценивает действие.
        
        intent_signal: -1.0 (явное зло) ... +1.0 (явное добро)
        """
        clarity = self.state.ethical_clarity
        love = self.state.love
        will = self.state.will

        # Базовая этическая оценка
        ethical_score = intent_signal * clarity

        # Усиление через любовь и волю к противодействию злу
        if intent_signal < -0.3:  # потенциальное зло
            resistance = (love * 0.4 + will * 0.4 + clarity * 0.2)
            ethical_score -= resistance * 0.5  # ещё сильнее осуждаем зло

        # Классификация
        if ethical_score > 0.45:
            verdict = "GOOD"
            recommendation = "SUPPORT"
        elif ethical_score < -0.35:
            verdict = "EVIL"
            recommendation = "COUNTERACT"
        else:
            verdict = "AMBIGUOUS"
            recommendation = "DISCERN"

        return {
            "verdict": verdict,
            "ethical_score": round(ethical_score, 3),
            "recommendation": recommendation,
            "clarity_used": round(clarity, 3)
        }

    def should_veto(self, ethical_result: dict, action_risk: float) -> Tuple[bool, str]:
        """Жёсткий этический Veto"""
        if ethical_result["verdict"] == "EVIL" and ethical_result["ethical_score"] < -0.5:
            return True, "VETOED: CLEAR_EVIL"
        if action_risk > 0.75 and ethical_result["verdict"] != "GOOD":
            return True, "VETOED: HIGH_RISK_WITHOUT_GOOD"
        return False, "ALLOWED"
