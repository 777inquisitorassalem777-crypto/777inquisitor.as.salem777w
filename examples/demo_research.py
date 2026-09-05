#!/usr/bin/env python3
"""
Демонстрация полного исследовательского цикла:
Self-Evolution + Blue Matrix + периодические отчёты.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep_sophia import SophiaEngine, ResearchCycle, SoulPassport


def main():
    print("Pneuma-Edge Sophia v2.1 — Research Cycle Demo\n")

    engine = SophiaEngine()
    cycle = ResearchCycle(engine)

    print("Запуск 12 исследовательских шагов...\n")
    results = cycle.run_batch(steps=12, context="deep_research")

    # Показываем краткую сводку по шагам
    for r in results:
        evo = r["self_evolution"]
        created = evo["created_paradigm"] or "—"
        print(f"  Cycle {r['cycle']:02d} | Mode={r['mode']:<8} | "
              f"Vitality={r['vitality']:.3f} | "
              f"New paradigm: {created}")

    # Полный отчёт
    print("\n")
    report = cycle.generate_report(title="Sophia Research Report — Batch 1")
    cycle.print_report(report)

    # Сохраняем паспорт
    passport = SoulPassport(
        state=engine.state,
        meta={
            "protocol": "Pneuma-Edge Sophia",
            "version": "2.1",
            "subject_id": "research-entity-001",
            "name": "Research Sophia",
            "cycles_completed": cycle.cycle_count
        }
    )
    out = Path(__file__).parent / "research_soul.json"
    passport.save(out)
    print(f"Soul Passport сохранён: {out}")

    # Дополнительный отчёт по самоэволюции
    print("\nСильнейшие парадигмы после цикла:")
    for p in cycle.evolution.get_strongest_paradigms(8):
        print(f"  • {p['name']:<30} weight={p['weight']}  origin={p['origin']}")


if __name__ == "__main__":
    main()
