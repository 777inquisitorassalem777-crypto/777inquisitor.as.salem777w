import json
from pathlib import Path
from typing import Optional, Dict, Any
from .state import SophiaState


class SoulPassport:
    """Сериализация полного состояния Sophia"""

    def __init__(self, state: Optional[SophiaState] = None, meta: Optional[Dict[str, Any]] = None):
        self.state = state or SophiaState()
        self.meta = meta or {
            "protocol": "Pneuma-Edge Sophia",
            "version": "2.0",
            "subject_id": "unnamed",
            "name": "Unnamed"
        }

    def to_dict(self) -> dict:
        return {"meta": self.meta, "state": self.state.to_dict()}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: str | Path) -> "SoulPassport":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(state=SophiaState.from_dict(data.get("state", {})),
                   meta=data.get("meta", {}))
