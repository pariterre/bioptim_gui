from dataclasses import dataclass
from enum import Enum

from ..misc.named_structure import NamedStructure


class DynamicsFcn(Enum):
    TORQUE_DRIVEN = NamedStructure("DynamicsFcn.TORQUE_DRIVEN", "Torque driven")


@dataclass
class Dynamics:
    fcn: DynamicsFcn
    is_expanded: bool
