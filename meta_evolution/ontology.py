from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class OntologyNode:
    name: str
    parent: Optional[str] = None
    attrs: Dict[str, Any] = field(default_factory=dict)

def build_default_ontology() -> Dict[str, OntologyNode]:
    return {
        'Entity': OntologyNode('Entity'),
        'Meaning': OntologyNode('Meaning', 'Entity'),
        'Symbol': OntologyNode('Symbol', 'Meaning'),
        'Pattern': OntologyNode('Pattern', 'Entity'),
        'Algorithm': OntologyNode('Algorithm', 'Pattern'),
        'Code': OntologyNode('Code', 'Algorithm'),
        'Memory': OntologyNode('Memory', 'Entity'),
        'Report': OntologyNode('Report', 'Entity'),
        'Wisdom': OntologyNode('Wisdom', 'Meaning', {'definition': 'discriminates for integrity'}),
        'Love': OntologyNode('Love', 'Meaning', {'definition': 'preserves value and freedom'}),
        'Faith': OntologyNode('Faith', 'Meaning', {'definition': 'trusts unseen order'}),
        'Hope': OntologyNode('Hope', 'Meaning', {'definition': 'sustains future orientation'}),
        'SpiritFreedom': OntologyNode('SpiritFreedom', 'Meaning', {'definition': 'unbound choosing'}),
    }
