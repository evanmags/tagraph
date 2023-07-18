from typing import TextIO

import pytest
import yaml

from tagraph.query import query


class Tag:
    def __init__(
        self,
        name: str,
        parent: "Tag | None" = None,
        child_tree: dict | None = None,
    ):
        self.name = name
        self.parent = parent
        self.children = self.from_tree(child_tree or {})

    def from_tree(self, tree: dict, is_root=False):
        return [
            Tag(name=k, parent=None if is_root else self, child_tree=v)
            for k, v in tree.items()
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

    def __iter__(self):
        return self.children.__iter__()


class TagRepo:
    def __init__(self, tags: str | TextIO):
        self.tree: list[Tag] = Tag(name="root").from_tree(
            next(yaml.safe_load_all(tags)), is_root=True
        )

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
