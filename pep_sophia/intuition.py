import random
from typing import List, Optional
from .state import SophiaState


class IntuitionModule:
    """
    Модуль интуиции и изобретательности.
    
    Сочетает:
    - принцип неопределённости (Heisenberg-like)
    - иррациональные скачки
    - нестандартные решения
    - "озарения" на основе текущего состояния мудрости и любви
    """

    def __init__(self, state: SophiaState):
        self.state = state

    def generate_insight(self, context: str = "") -> str:
        """Генерирует интуитивное озарение / нестандартный ход"""
        seed = (self.state.intuition * 0.4 +
                self.state.wisdom * 0.3 +
                self.state.love * 0.2 +
                (1.0 - self.state.uncertainty) * 0.1)

        # Иррациональный компонент
        chaos = random.uniform(0, 1 - seed) * self.state.uncertainty

        templates = [
            "Иногда путь открывается только когда перестаёшь искать прямой.",
            "Истинная сила — в способности не отвечать злом на зло, но и не быть слабым.",
            "То, что кажется хаосом, может быть высшим порядком, ещё не распознанным.",
            "Любовь без воли становится бессильной. Воля без любви — жестокой.",
            "Неопределённость — не враг, а пространство, в котором рождается новое.",
            "Мудрость предков живёт не в буквах, а в способности слышать.",
            "Противодействие злу начинается с ясности внутри.",
            "Изобретательность рождается на границе известного и неизвестного.",
        ]

        # Выбираем в зависимости от состояния
        idx = int((seed + chaos) * len(templates)) % len(templates)
        insight = templates[idx]

        if context:
            insight = f"В контексте «{context[:60]}...»: {insight}"

        # Записываем в состояние
        self.state.last_insights = ([insight] + self.state.last_insights)[:7]
        return insight

    def non_standard_solution(self, problem: str) -> dict:
        """Предлагает нестандартный подход к задаче"""
        inventiveness = self.state.inventiveness
        uncertainty = self.state.uncertainty

        approach = "linear"
        if inventiveness > 0.6 and uncertainty > 0.3:
            approach = "lateral"
        elif inventiveness > 0.75:
            approach = "paradigm_shift"
        elif uncertainty > 0.7:
            approach = "embrace_chaos"

        return {
            "problem": problem[:100],
            "recommended_approach": approach,
            "inventiveness_level": round(inventiveness, 3),
            "insight": self.generate_insight(problem)
        }
