from dataclasses import dataclass
from enum import Enum

from ..misc.named_structure import NamedStructure


@dataclass
class NamedStructureWithExtension(NamedStructure):
    extension: str


class BioModels(Enum):
    BIORBD = NamedStructureWithExtension("BiorbdModel", "Biorbd", "bioMod")
    DUMMY = NamedStructureWithExtension("DummyModel", "Dummy", "dummy")
