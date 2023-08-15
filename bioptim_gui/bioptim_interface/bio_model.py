from enum import Enum

from ..misc.named_structure import NamedStructure


class BioModels(Enum):
    BIORBD = NamedStructure("BiorbdModel", "Model from Biorbd")
