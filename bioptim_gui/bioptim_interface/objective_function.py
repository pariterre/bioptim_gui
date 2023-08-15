from dataclasses import dataclass, field
from enum import Enum

from ..misc.named_structure import NamedStructure


class ObjectiveFunctionFcn:
    class Lagrange(Enum):
        MINIMIZE_CONTROL = NamedStructure("ObjectiveFcn.Lagrange.MINIMIZE_CONTROL", "Minimize controls")

    class Mayer(Enum):
        MINIMIZE_TIME = NamedStructure("ObjectiveFcn.Mayer.MINIMIZE_TIME", "Minimize time")


@dataclass
class ObjectiveFunction:
    fcn: ObjectiveFunctionFcn.Lagrange | ObjectiveFunctionFcn.Mayer
    args: dict = field(default_factory=dict)
