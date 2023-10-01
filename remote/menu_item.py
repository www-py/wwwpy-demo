from dataclasses import dataclass, field
from typing import Union, List


@dataclass(frozen=True)
class MenuItem:
    caption: str
    parent: Union['MenuItem', None] = None
    children: List['MenuItem'] = field(default_factory=list)
    action: Union[callable, None] = None

    def new_child(self, caption, action=None):
        item = MenuItem(caption, self, action=action)
        self.children.append(item)
        return item
