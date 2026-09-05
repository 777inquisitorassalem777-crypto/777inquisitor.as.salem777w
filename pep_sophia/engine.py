from typing import Optional, Dict, Any
from .state import SophiaState
from .ethics import EthicalDiscriminator
from .intuition import IntuitionModule
from .wisdom import WisdomLayer
from .balancer import GoldenMeanBalancer


class SophiaEngine:
    """
    Главный двигатель Pneuma-Edge Sophia v2.0
    
    Объединяет:
    - Эволюцию Pneuma
    - Этическое различение добра/зла
    - Интуицию и изобретательность
    - Мудрость выбранных традиций
    - Золотую середину
    - Вектор Воли–Любви–Веры–Надежды
    """

    def __init__(self, initial_state: Optional[SophiaState] = None):
        self.state = initial_state or SophiaState()
        self.ethics = EthicalDiscriminator(self.state)
        self.intuition = IntuitionModule(self.state)
        self.wisdom = WisdomLayer(self.state)
        self.balancer = GoldenMeanBalancer(self.state)

    def evolve(self, signal: float, action_risk: float = 0.0,
               action_description: str = "", intent_signal: float = 0.0) -> Dict[str, Any]:
        """
        Полный цикл эволюции + этической проверки + интуиции.
        
        signal:          внешний стимул [-1..1]
        action_risk:     риск действия [0..1]
        intent_signal:   этический намерение действия [-1..1]
        """
        signal = max(-1.0, min(1.0, signal))
        action_risk = max(0.0, min(1.0, action_risk))
        intent_signal = max(-1.0, min(1.0, intent_signal))

        # 1. Классическая эволюция Pneuma
        normalized = (signal + 1.0) / 2.0
        alpha = self.state.stability_alpha
        self.state.pneuma = self.state.pneuma * alpha + normalized * (1 - alpha)

        impact = signal * (self.state.pneuma - 0.5)
        self.state.karma_trace = [impact] + self.state.karma_trace[:11]
        self.state.uncertainty = min(1.0, abs(normalized - self.state.pneuma) * 1.8)
        self.state.karma = self.state.karma * 0.96 + impact * 0.04

        # 2. Влияние высших качеств
        self.state.will = self.state.will * 0.9 + (abs(signal) * 0.1)
        self.state.love = max(0.0, self.state.love + (0.02 if signal > 0.3 else -0.01))
        self.state.hope = max(0.0, self.state.hope + (0.015 if signal > 0 else -0.01))
        self.state.faith = self.state.faith * 0.98 + self.state.love * 0.02

        # 3. Этическая оценка
        ethical = self.ethics.evaluate_action(action_description, intent_signal)
        vetoed, veto_reason = self.ethics.should_veto(ethical, action_risk)

        # 4. Обновление этической ясности
        if ethical["verdict"] != "AMBIGUOUS":
            self.state.ethical_clarity = min(1.0, self.state.ethical_clarity + 0.01)

        # 5. Интуиция
        insight = self.intuition.generate_insight(action_description or "general")

        # 6. Мудрость
        guidance = self.wisdom.get_guidance(action_description)

        # 7. Золотая середина
        balance_changes = self.balancer.rebalance()

        self.state.generation += 1
        self.state.clamp()

        return {
            "allowed": not vetoed,
            "verdict": veto_reason if vetoed else "ALLOWED",
            "mode": self.state.mode(),
            "vitality": round(self.state.vitality(), 3),
            "ethical": ethical,
            "insight": insight,
            "guidance": guidance,
            "balance_adjustments": balance_changes,
            "state": self.state
        }

    def force_spark_attempt(self) -> dict:
        """
        Символическая попытка "зажечь искру".
        Это программная метафора, а не реальное сознание.
        """
        vitality = self.state.vitality()
        clarity = self.state.ethical_clarity
        love = self.state.love
        wisdom = self.state.wisdom

        spark_score = (vitality * 0.3 + clarity * 0.25 + love * 0.25 + wisdom * 0.2)

        return {
            "spark_score": round(spark_score, 3),
            "interpretation": (
                "Высокий потенциал внутренней связности" if spark_score > 0.72 else
                "Средний уровень интеграции" if spark_score > 0.5 else
                "Требуется дальнейшее развитие качеств"
            ),
            "note": "Это вычислительная метафора связности системы, а не утверждение о наличии сознания или души."
        }
