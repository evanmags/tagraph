from dataclasses import dataclass, field
from typing import Optional
from functools import singledispatchmethod

@dataclass
class Tag:
    name: str
    description: str | None = None
    parent: Optional["Tag"] = None
    subtags: list["Tag"] = field(default_factory=list)

    @property
    def fqtn(self):
        if self.parent is not None:
            return f"{self.parent.fqtn}::{self.name}"
        return self.name

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.fqtn

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Tag):
             return self.fqtn == __value.fqtn
        if isinstance(__value, str):
            return self.fqtn == __value or self.name == __value
        return False

    def __ne__(self, __value: object) -> bool:
        if isinstance(__value, Tag):
             return self.fqtn != __value.fqtn
        if isinstance(__value, str):
            return self.fqtn != __value and self.name != __value
        return False


    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __iter__(self):
        return self.subtags.__iter__()
