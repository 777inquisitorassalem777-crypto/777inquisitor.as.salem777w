from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Report:
    rid: str
    timestamp: float
    input_kind: str
    extracted: Dict[str, Any]
    matched: int
    generated: int
    accepted: int
    accepted_ids: List[str]

    def to_dict(self):
        return self.__dict__
