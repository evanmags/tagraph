import yaml
from typing import TextIO

from tagraph.tag import Tag
from tagraph.tree import Tree

class TagRepo:
    def __init__(self, tags: str | TextIO):
        self.tree: Tree[Tag] = self.load_tags(next(yaml.safe_load_all(tags)))
    
    def load_tags(self, tree: dict) -> Tree[Tag]:
        ts = []
        for key in tree:
            p = Tag(
                name=key
            )
            if tree[key] is not None:
                for c in self.load_tags(tree[key]):
                    c.parent = p
                    p.subtags.append(c)

            ts.append(p)
        return Tree(ts)

    def query(self, q: str) -> list[Tag]:
        return self.tree.query(q)
