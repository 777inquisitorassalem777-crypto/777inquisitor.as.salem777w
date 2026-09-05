import time, uuid, logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from .ontology import build_default_ontology
from .reporting import Report
from .storage import save_json, load_json

@dataclass
class InputItem:
    kind: str
    payload: Any
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Candidate:
    cid: str
    kind: str
    content: Any
    scores: Dict[str, float] = field(default_factory=dict)
    accepted: bool = False

class MetaEvolutionCore:
    def __init__(self, config):
        self.config = config
        self.ontology = build_default_ontology()
        self.memory_file = self.config.data_dir / 'memory.json'
        self.registry_file = self.config.data_dir / 'registry.json'
        self.reports_file = self.config.data_dir / 'reports.json'
        self.memory: List[InputItem] = []
        self.registry: List[Candidate] = []
        self.reports: List[Report] = []
        self.logger = logging.getLogger('meta_evolution')
        self._load_state()

    def _load_state(self):
        for x in load_json(self.memory_file, []):
            self.memory.append(InputItem(**x))
        for x in load_json(self.registry_file, []):
            self.registry.append(Candidate(**x))
        for x in load_json(self.reports_file, []):
            self.reports.append(Report(**x))

    def _save_state(self):
        save_json(self.memory_file, [x.__dict__ for x in self.memory])
        save_json(self.registry_file, [x.__dict__ for x in self.registry])
        save_json(self.reports_file, [x.__dict__ for x in self.reports])

    def ingest(self, item: InputItem):
        self.memory.append(item)
        self._save_state()

    def extract_features(self, item: InputItem) -> Dict[str, Any]:
        text = str(item.payload)
        return {'meaning': text[:256], 'symbols': [ch for ch in set(text) if not ch.isalnum()], 'constraints': item.meta.get('constraints', {}), 'risks': {'binary_trap': (' или ' in text.lower())}, 'intent': item.meta.get('intent', '')}

    def match_memory(self, features: Dict[str, Any]) -> List[InputItem]:
        return list(self.memory)

    def generate_candidates(self, item: InputItem, features: Dict[str, Any], matches: List[InputItem]) -> List[Candidate]:
        return [Candidate(str(uuid.uuid4()), k, {'source': item.kind, 'seed': features['meaning'][:40]}) for k in ('rule','pattern','algorithm','code')]

    def validate(self, candidate: Candidate) -> Tuple[bool, Dict[str, float]]:
        scores = {'usefulness': 0.8, 'stability': 0.8, 'reproducibility': 0.8, 'ethics': 0.8, 'compatibility': 0.8}
        candidate.scores = scores
        candidate.accepted = all(v >= self.config.acceptance_threshold for v in scores.values())
        return candidate.accepted, scores

    def store(self, candidates: List[Candidate]):
        for c in candidates:
            if c.accepted:
                self.registry.append(c)
        self._save_state()

    def cycle(self, item: InputItem) -> Report:
        self.ingest(item)
        features = self.extract_features(item)
        matches = self.match_memory(features)
        candidates = self.generate_candidates(item, features, matches)
        for c in candidates:
            self.validate(c)
        self.store(candidates)
        rep = Report(str(uuid.uuid4()), time.time(), item.kind, features, len(matches), len(candidates), len([c for c in candidates if c.accepted]), [c.cid for c in candidates if c.accepted])
        self.reports.append(rep)
        self._save_state()
        self.logger.info('cycle complete input=%s generated=%s accepted=%s', item.kind, rep.generated, rep.accepted)
        return rep
