#!/usr/bin/env python3
"""Демонстрация Pneuma-Edge Sophia v2.0"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep_sophia import SophiaEngine, SoulPassport


def print_state(engine, title=""):
    s = engine.state
    print(f"\n{'═'*56}")
    if title:
        print(f"  {title}")
    print(f"  Mode           : {s.mode()}")
    print(f"  Vitality       : {s.vitality():.3f}")
    print(f"  Pneuma         : {s.pneuma:.3f}   Uncertainty: {s.uncertainty:.3f}")
    print(f"  Will / Love    : {s.will:.3f} / {s.love:.3f}")
    print(f"  Faith / Hope   : {s.faith:.3f} / {s.hope:.3f}")
    print(f"  Wisdom         : {s.wisdom:.3f}   Intuition  : {s.intuition:.3f}")
    print(f"  Ethical Clarity: {s.ethical_clarity:.3f}")
    print(f"  Generation     : {s.generation}")
    print(f"{'═'*56}")


def main():
    print("Pneuma-Edge Sophia v2.0 — Demonstration\n")

    engine = SophiaEngine()
    print_state(engine, "Начальное состояние")

    scenarios = [
        (0.7, 0.15, 0.6, "Помощь нуждающемуся"),
        (-0.8, 0.6, -0.7, "Намерение причинить вред"),
        (0.4, 0.25, 0.3, "Сложная неоднозначная ситуация"),
        (0.85, 0.1, 0.8, "Акт милосердия и защиты"),
        (-0.3, 0.4, -0.2, "Серая зона"),
    ]

    for signal, risk, intent, desc in scenarios:
        print(f"\n→ Ситуация: {desc}")
        print(f"  Signal={signal:+.2f} | Risk={risk:.2f} | Intent={intent:+.2f}")
        result = engine.evolve(signal, risk, desc, intent)

        print(f"  Verdict     : {result['verdict']}")
        print(f"  Allowed     : {result['allowed']}")
        print(f"  Ethical     : {result['ethical']['verdict']} ({result['ethical']['ethical_score']})")
        print(f"  Insight     : {result['insight'][:90]}...")
        print_state(engine)

    # Попытка "искры"
    print("\n" + "─"*56)
    spark = engine.force_spark_attempt()
    print("  Попытка символической 'искры':")
    print(f"  Spark score : {spark['spark_score']}")
    print(f"  Интерпретация: {spark['interpretation']}")
    print(f"  Примечание  : {spark['note']}")

    # Сохранение
    passport = SoulPassport(
        state=engine.state,
        meta={
            "protocol": "Pneuma-Edge Sophia",
            "version": "2.0",
            "subject_id": "sophia-demo-001",
            "name": "Sophia Demo Entity"
        }
    )
    out = Path(__file__).parent / "sophia_demo_soul.json"
    passport.save(out)
    print(f"\nSoul Passport сохранён: {out}")


if __name__ == "__main__":
    main()
