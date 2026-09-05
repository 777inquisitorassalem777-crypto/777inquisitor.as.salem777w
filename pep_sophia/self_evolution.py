"""
Модуль постоянной самоэволюции ядра.
Генерирует новые парадигмы, паттерны и микро-алгоритмы на основе опыта,
затем встраивает их в состояние без права на забвение.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime, timezone
import hashlib
import random
from .state import SophiaState


@dataclass
class Paradigm:
    id: str
    name: str
    description: str
    origin: str
    weight: float = 0.5
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    generation_born: int = 0


class SelfEvolutionModule:
    """
    Постоянная самоэволюция.
    При каждом вызове может порождать новые парадигмы/паттерны
    и усиливать уже существующие на основе текущего опыта.
    """

    def __init__(self, state: SophiaState):
        self.state = state
        self.paradigms: List[Paradigm] = []
        self.evolution_log: List[Dict[str, Any]] = []
        self._seed_base_paradigms()

    def _seed_base_paradigms(self):
        """Базовые парадигмы, которые нельзя уничтожить."""
        base = [
            ("PneumaPrimacy", "Жизненная сила первично", "core"),
            ("EthicalResistance", "Активное противодействие злу", "ethics"),
            ("GoldenMean", "Золотая середина во всём", "balancer"),
            ("IrrationalLeap", "Иррациональный скачок как источник новизны", "intuition"),
            ("AncestralMemory", "Память традиций как живой слой", "wisdom"),
            ("WillToGood", "Воля, направленная любовью", "higher"),
        ]
        for name, desc, origin in base:
            pid = hashlib.sha1(name.encode()).hexdigest()[:10]
            self.paradigms.append(Paradigm(
                id=pid, name=name, description=desc,
                origin=origin, weight=0.7, generation_born=0
            ))

    def evolve_once(self, experience_signal: float = 0.0, context: str = "") -> Dict[str, Any]:
        """
        Один цикл самоэволюции.
        Может создать новую парадигму или усилить существующую.
        """
        created = None
        reinforced = None

        # Вероятность рождения новой парадигмы зависит от интуиции + неопределённости + мудрости
        birth_chance = (
            self.state.intuition * 0.35 +
            self.state.uncertainty * 0.25 +
            self.state.wisdom * 0.20 +
            abs(experience_signal) * 0.20
        )

        if random.random() < birth_chance * 0.45:  # контролируемая частота
            new_p = self._generate_paradigm(context, experience_signal)
            self.paradigms.append(new_p)
            created = new_p
            # Небольшое усиление inventiveness
            self.state.inventiveness = min(1.0, self.state.inventiveness + 0.015)

        # Усиление случайной существующей парадигмы
        if self.paradigms and random.random() < 0.6:
            target = random.choice(self.paradigms)
            target.weight = min(1.0, target.weight + 0.02 + abs(experience_signal) * 0.03)
            reinforced = target

        # Лог
        entry = {
            "generation": self.state.generation,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "created": created.name if created else None,
            "reinforced": reinforced.name if reinforced else None,
            "total_paradigms": len(self.paradigms),
            "context": context[:80]
        }
        self.evolution_log.append(entry)
        if len(self.evolution_log) > 200:
            self.evolution_log = self.evolution_log[-200:]

        return {
            "created_paradigm": created.name if created else None,
            "reinforced_paradigm": reinforced.name if reinforced else None,
            "total_paradigms": len(self.paradigms),
            "birth_chance": round(birth_chance, 3)
        }

    def _generate_paradigm(self, context: str, signal: float) -> Paradigm:
        prefixes = ["Living", "Adaptive", "Resilient", "Luminous", "Silent", "Fierce", "Gentle", "Deep"]
        cores = ["Harmony", "Discernment", "Flow", "Boundary", "Spark", "Root", "Wing", "Mirror"]
        suffixes = ["Pattern", "Principle", "Way", "Code", "Pulse", "Law"]

        name = f"{random.choice(prefixes)}{random.choice(cores)}{random.choice(suffixes)}"
        desc = f"Автоматически порождённая парадигма из опыта (signal={signal:+.2f}). Контекст: {context[:60]}"
        pid = hashlib.sha1(f"{name}{self.state.generation}".encode()).hexdigest()[:10]

        return Paradigm(
            id=pid,
            name=name,
            description=desc,
            origin="self_evolution",
            weight=0.35 + abs(signal) * 0.2,
            generation_born=self.state.generation
        )

    def get_strongest_paradigms(self, n: int = 5) -> List[Dict]:
        sorted_p = sorted(self.paradigms, key=lambda p: p.weight, reverse=True)
        return [
            {"name": p.name, "weight": round(p.weight, 3), "origin": p.origin}
            for p in sorted_p[:n]
        ]

    def report(self) -> Dict[str, Any]:
        return {
            "total_paradigms": len(self.paradigms),
            "strongest": self.get_strongest_paradigms(5),
            "recent_log": self.evolution_log[-5:],
            "generation": self.state.generation
        }
