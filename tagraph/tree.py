from typing import Generic, Iterable, TypeVar
from tagraph.query import query, Queryable

T = TypeVar("T", bound=Queryable)

class Tree(Generic[T]):
    def __init__(self, children: Iterable[T]) -> None:
        self.children = children

    def __iter__(self):
        return self.children.__iter__()

    def __repr__(self) -> str:
        return str([c for c in self.children])

    def query(self, q: str) -> list[T]:
        return query(q)(self)
