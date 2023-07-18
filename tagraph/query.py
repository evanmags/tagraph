from typing import Iterable, Protocol, Generic, TypeVar, Any
from itertools import chain

QT = TypeVar("QT", covariant=True)


class Queryable(Generic[QT], Protocol):
    def __iter__(self) -> QT:
        ...

    def __eq__(self, __value: str) -> bool:
        ...


T = TypeVar("T", bound=Queryable)


class query(Generic[T]):
    def __init__(self, q: str):
        _self, _next = q, None
        if "::" in q:
            _self, _next = q.split("::", 1)

        self.part = query_part(_self.strip("{} "))
        self.next = query(_next) if _next is not None else None

    def __call__(self, graph: Queryable[T]) -> list[T]:
        result = self.part.get_matches(graph)
        if self.next:
            return self.next(chain.from_iterable(result))

        return result

    def __repr__(self) -> str:
        p = str(self.part)
        if self.part:
            return f"{p}::{repr(self.next)}"
        return p


def query_part(part: str) -> "__query_part":
    if "&" in part:
        return query__and(*part.split("&", 1))
    elif "|" in part:
        return query__or(*part.split("|", 1))
    elif part.startswith("!"):
        return query__not(part[1:])
    elif part == "*":
        return query__wildcard()
    elif part == "**":
        return query__multi_level_wildcard()
    else:
        return query__name(part)


class __query_part:
    def get_matches(self, graph: Queryable):
        return [t for t in graph if self == t]


class query__or(__query_part):
    def __init__(self, *parts: str):
        self.__parts = list(query_part(p) for p in parts)

    def __eq__(self, other):
        return any(p == other for p in self.__parts)

    def __repr__(self) -> str:
        return "|".join(repr(p) for p in self.__parts)


class query__and(__query_part):
    def __init__(self, *parts: str):
        self.__parts = list(query_part(p) for p in parts)

    def __eq__(self, other):
        return all(p == other for p in self.__parts)

    def __repr__(self) -> str:
        return "&".join(repr(p) for p in self.__parts)


class query__not(__query_part):
    def __init__(self, part: str):
        self.__part = query_part(part)

    def __eq__(self, other) -> bool:
        return self.__part != other

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"!{self.__part}"


class query__name(str, (__query_part)):
    def __init__(self, part: str):
        self.__part = part

    def __eq__(self, __value: object) -> bool:
        return __value == self.__part

    def __ne__(self, __value: object) -> bool:
        return __value != self.__part

    def __repr__(self) -> str:
        return self.__part


class query__wildcard(__query_part):
    def __repr__(self) -> str:
        return "*"

    def __eq__(self, __value: object) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False


class query__multi_level_wildcard(__query_part):
    def __repr__(self) -> str:
        return "**"

    def get_matches(self, graph: Iterable):
        _next = [c for c in graph]
        _return = []
        for i in _next:
            _return.append(i)
            _next += [_i for _i in i if _i not in _next]

        return list(_return)
