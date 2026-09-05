"""
Pneuma-Edge Sophia Core v2.1
Symbiotic architecture + Self-Evolution + Blue Matrix + Research Cycle
"""

from .state import SophiaState
from .engine import SophiaEngine
from .ethics import EthicalDiscriminator
from .intuition import IntuitionModule
from .wisdom import WisdomLayer
from .balancer import GoldenMeanBalancer
from .passport import SoulPassport
from .self_evolution import SelfEvolutionModule, Paradigm
from .blue_matrix import BlueMatrix, SensorReading
from .research_cycle import ResearchCycle

__version__ = "2.1.0"
__all__ = [
    "SophiaState",
    "SophiaEngine",
    "EthicalDiscriminator",
    "IntuitionModule",
    "WisdomLayer",
    "GoldenMeanBalancer",
    "SoulPassport",
    "SelfEvolutionModule",
    "Paradigm",
    "BlueMatrix",
    "SensorReading",
    "ResearchCycle",
]
