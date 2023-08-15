from dataclasses import dataclass


@dataclass
class NamedStructure:
    interface_name: str
    pretty_name: str

    def __repr__(self):
        return self.interface_name

    def __str__(self):
        return self.pretty_name
