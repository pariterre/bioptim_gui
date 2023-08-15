from enum import Enum

from ..misc.named_structure import NamedStructure


class OptimalControlType(Enum):
    OptimalControlProgram = NamedStructure("OptimalControlProgram", "Optimal control program")
