from dataclasses import dataclass, field, asdict
from typing import List, Dict
import json
from datetime import datetime, timezone


@dataclass
class SophiaState:
    """
    Extended state vector of Pneuma-Edge Sophia.
    
    Core:
        P - Pneuma (vital stability / agency)
        U - Uncertainty (entropy + Heisenberg-like principle)
        K - Karma (long-term ethical imprint)
    
    Higher faculties:
        Will, Love, Faith, Hope
        Wisdom (aggregated from allowed traditions)
        Intuition
        Ethical_clarity (ability to distinguish good / evil)
    """
    # === Core Pneuma layer ===
    pneuma: float = 0.55
    uncertainty: float = 0.25
    karma: float = 0.1
    generation: int = 0
    stability_alpha: float = 0.82

    # === Higher vector ===
    will: float = 0.5          # способность действовать по своему усмотрению
    love: float = 0.5
    faith: float = 0.5
    hope: float = 0.5

    # === Derived / emergent ===
    wisdom: float = 0.5        # агрегат мудрости традиций
    intuition: float = 0.4
    ethical_clarity: float = 0.6   # ясность различения добра и зла
    inventiveness: float = 0.45

    # === Internal memory ===
    karma_trace: List[float] = field(default_factory=lambda: [0.0] * 12)
    last_insights: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def clamp(self) -> None:
        for attr in ["pneuma", "uncertainty", "will", "love", "faith", "hope",
                     "wisdom", "intuition", "ethical_clarity", "inventiveness"]:
            val = getattr(self, attr)
            setattr(self, attr, max(0.0, min(1.0, float(val))))
        self.karma = max(-1.0, min(1.0, float(self.karma)))
        self.generation = max(0, int(self.generation))

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "SophiaState":
        known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known)

    def mode(self) -> str:
        if self.uncertainty > 0.68:
            return "CRISIS"
        if self.pneuma > 0.78 and self.uncertainty < 0.28 and self.love > 0.6:
            return "FLOW"
        if self.ethical_clarity > 0.75 and self.will > 0.65:
            return "RESOLUTE"
        return "STABLE"

    def vitality(self) -> float:
        """Общая жизненная сила субъекта"""
        return (self.pneuma * 0.35 +
                self.will * 0.15 +
                self.love * 0.15 +
                self.faith * 0.1 +
                self.hope * 0.1 +
                self.wisdom * 0.15)
