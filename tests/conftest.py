import pytest
import yaml
from typing import TextIO, TypeVar

from tagraph.query import query, Queryable

T = TypeVar("T", bound=Queryable)


class Tag:
    def __init__(
        self,
        name: str,
        parent: "Tag | None" = None,
        child_tree: dict | None = None,
    ):
        self.name = name
        self.parent = parent
        self.children = [
            Tag(name=k, parent=self, child_tree=v)
            for k, v in (child_tree or {}).items()
        ]

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
        return self.children.__iter__()


class TagRepo:
    def __init__(self, tags: str | TextIO):
        self.tree: list[Tag] = self.load_tags(next(yaml.safe_load_all(tags)))

    def load_tags(self, tree: dict) -> list[Tag]:
        return [Tag(name=k, parent=None, child_tree=v) for k, v in tree.items()]

    def query(self, q: str) -> list[Tag]:
        return query(q)(self.tree)


TAGS = """
funny:
  fail:
    injury:
  video:
  joke:
    video:
    knock-knock:
    dad:
      good:
      bad:
science:
  pop:
  biology:
    micro:
    neuro:
"""

@pytest.fixture
def repo() -> TagRepo:
    return TagRepo(TAGS)
