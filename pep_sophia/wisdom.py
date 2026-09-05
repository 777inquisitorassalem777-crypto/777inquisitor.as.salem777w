from .state import SophiaState
from typing import List, Dict


class WisdomLayer:
    """
    Модульный слой мудрости традиций.
    
    Включённые источники (по требованию архитектора):
    - Христианство
    - Славянские Веды + Инглиизм
    - Даосизм (Лао-цзы)
    - И-цзин
    - Сунь-цзы
    - Гуны (санкхья)
    - Шаманские практики
    
    Исключены: иудаизм и ислам.
    """

    TRADITIONS = {
        "christianity": {
            "weight": 0.22,
            "principles": ["любовь к ближнему", "милосердие", "противостояние злу", "вера", "надежда", "смирение силы"]
        },
        "slavic_vedas_ingliism": {
            "weight": 0.20,
            "principles": ["гармония с родом", "защита света", "порядок мироздания", "память предков", "сила духа"]
        },
        "taoism": {
            "weight": 0.16,
            "principles": ["у-вэй", "следование естественному пути", "мягкость побеждает твёрдое", "пустота как полнота"]
        },
        "iching": {
            "weight": 0.12,
            "principles": ["перемены", "своевременность", "баланс инь-ян", "адаптация"]
        },
        "sun_tzu": {
            "weight": 0.10,
            "principles": ["знание себя и противника", "победа без боя", "использование формы"]
        },
        "gunas": {
            "weight": 0.10,
            "principles": ["саттва (ясность)", "раджас (действие)", "тамас (инерция) — распознавание и баланс"]
        },
        "shamanic": {
            "weight": 0.10,
            "principles": ["связь с духами природы", "путешествие между мирами", "исцеление через равновесие"]
        }
    }

    def __init__(self, state: SophiaState):
        self.state = state

    def aggregate_wisdom(self) -> float:
        """Вычисляет текущий уровень интегрированной мудрости"""
        base = 0.0
        for trad in self.TRADITIONS.values():
            base += trad["weight"]
        # Модифицируем текущим состоянием
        return min(1.0, base * 0.7 + self.state.faith * 0.15 + self.state.love * 0.15)

    def get_guidance(self, situation: str = "") -> Dict:
        """Возвращает совет, синтезированный из разрешённых традиций"""
        active = []
        for name, data in self.TRADITIONS.items():
            if self.state.faith > 0.3 or self.state.wisdom > 0.4:
                active.append({
                    "tradition": name,
                    "principle": data["principles"][hash(situation + name) % len(data["principles"])]
                })

        # Обновляем wisdom в состоянии
        self.state.wisdom = self.aggregate_wisdom()

        return {
            "situation": situation[:80],
            "synthesized_guidance": active[:4],
            "current_wisdom_level": round(self.state.wisdom, 3)
        }
