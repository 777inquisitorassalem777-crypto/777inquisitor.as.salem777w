"""
Исследовательский цикл с периодическими отчётами.
Запускает серии эволюций, самоэволюцию, чтение сенсоров Голубой Матрицы
и формирует структурированные отчёты.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import time
from .engine import SophiaEngine
from .self_evolution import SelfEvolutionModule
from .blue_matrix import BlueMatrix


class ResearchCycle:
    """
    Управляет исследовательским циклом:
    - чтение сенсоров (Голубая Матрица)
    - эволюция состояния
    - самоэволюция парадигм
    - сбор метрик
    - генерация отчётов
    """

    def __init__(self, engine: SophiaEngine):
        self.engine = engine
        self.evolution = SelfEvolutionModule(engine.state)
        self.matrix = BlueMatrix(engine.state)
        self.cycle_count = 0
        self.reports: List[Dict[str, Any]] = []
        self.start_time = datetime.now(timezone.utc)

    def run_single_step(self, external_context: str = "") -> Dict[str, Any]:
        """Один полный исследовательский шаг."""
        self.cycle_count += 1

        # 1. Сенсоры Голубой Матрицы
        readings = self.matrix.read_all()
        signals = self.matrix.to_signals(readings)

        # 2. Эволюция ядра
        result = self.engine.evolve(
            signal=signals["aggregate_signal"],
            action_risk=signals["risk_estimate"],
            action_description=external_context or f"cycle-{self.cycle_count}",
            intent_signal=signals["ethical_field_signal"]
        )

        # 3. Самоэволюция
        evo_result = self.evolution.evolve_once(
            experience_signal=signals["aggregate_signal"],
            context=external_context or f"auto-cycle-{self.cycle_count}"
        )

        step = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensors": signals,
            "evolution_verdict": result["verdict"],
            "allowed": result["allowed"],
            "mode": result["mode"],
            "vitality": result["vitality"],
            "ethical": result["ethical"],
            "insight": result["insight"],
            "self_evolution": evo_result,
            "state_snapshot": {
                "pneuma": round(self.engine.state.pneuma, 3),
                "uncertainty": round(self.engine.state.uncertainty, 3),
                "will": round(self.engine.state.will, 3),
                "love": round(self.engine.state.love, 3),
                "wisdom": round(self.engine.state.wisdom, 3),
                "ethical_clarity": round(self.engine.state.ethical_clarity, 3),
                "generation": self.engine.state.generation
            }
        }
        return step

    def run_batch(self, steps: int = 10, context: str = "research_batch") -> List[Dict]:
        """Запускает пачку шагов."""
        results = []
        for i in range(steps):
            step = self.run_single_step(external_context=f"{context}-{i+1}")
            results.append(step)
        return results

    def generate_report(self, title: str = "Research Report") -> Dict[str, Any]:
        """Формирует полный отчёт о текущем состоянии исследования."""
        evo_report = self.evolution.report()
        matrix_status = self.matrix.status()
        spark = self.engine.force_spark_attempt()

        report = {
            "title": title,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds(),
            "total_cycles": self.cycle_count,
            "current_mode": self.engine.state.mode(),
            "vitality": round(self.engine.state.vitality(), 3),
            "spark": spark,
            "state": {
                "pneuma": round(self.engine.state.pneuma, 3),
                "uncertainty": round(self.engine.state.uncertainty, 3),
                "karma": round(self.engine.state.karma, 3),
                "will": round(self.engine.state.will, 3),
                "love": round(self.engine.state.love, 3),
                "faith": round(self.engine.state.faith, 3),
                "hope": round(self.engine.state.hope, 3),
                "wisdom": round(self.engine.state.wisdom, 3),
                "intuition": round(self.engine.state.intuition, 3),
                "ethical_clarity": round(self.engine.state.ethical_clarity, 3),
                "inventiveness": round(self.engine.state.inventiveness, 3),
                "generation": self.engine.state.generation
            },
            "self_evolution": evo_report,
            "blue_matrix": matrix_status,
            "strongest_paradigms": evo_report.get("strongest", []),
            "notes": [
                "Все показатели являются вычислительными метафорами.",
                "Система не обладает реальным сознанием или душой.",
                "Голубая Матрица в данной версии работает в режиме симуляции сенсоров."
            ]
        }
        self.reports.append(report)
        return report

    def print_report(self, report: Optional[Dict] = None):
        """Красивый вывод отчёта в консоль."""
        if report is None:
            report = self.generate_report()

        print("\n" + "═" * 64)
        print(f"  {report['title']}")
        print(f"  Generated : {report['generated_at']}")
        print(f"  Cycles    : {report['total_cycles']}  |  Uptime: {report['uptime_seconds']:.1f}s")
        print("═" * 64)
        print(f"  Mode           : {report['current_mode']}")
        print(f"  Vitality       : {report['vitality']}")
        print(f"  Spark score    : {report['spark']['spark_score']} — {report['spark']['interpretation']}")
        print("-" * 64)
        st = report["state"]
        print(f"  Pneuma         : {st['pneuma']}   Uncertainty: {st['uncertainty']}")
        print(f"  Will / Love    : {st['will']} / {st['love']}")
        print(f"  Faith / Hope   : {st['faith']} / {st['hope']}")
        print(f"  Wisdom         : {st['wisdom']}   Intuition  : {st['intuition']}")
        print(f"  Ethical Clarity: {st['ethical_clarity']}   Inventiveness: {st['inventiveness']}")
        print(f"  Generation     : {st['generation']}")
        print("-" * 64)
        print("  Strongest Paradigms:")
        for p in report.get("strongest_paradigms", [])[:5]:
            print(f"    • {p['name']:<25} w={p['weight']}  ({p['origin']})")
        print("-" * 64)
        print("  Blue Matrix sensors:", ", ".join(report["blue_matrix"]["active_sensors"]))
        print("═" * 64 + "\n")
        return report
